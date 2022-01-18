from abc import ABC, abstractmethod

import session_handler.file_finder as ff
from storages.backends.gcloud import GoogleCloudStorage

# 3. File upload
storage = GoogleCloudStorage()
from abc import ABC, abstractmethod
from typing import Any, Optional


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: "Handler") -> "Handler":
        pass

    @abstractmethod
    def handle(self, request, parameters) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any, parameters) -> str:
        if self._next_handler:
            return self._next_handler.handle(request, parameters)

        return None


"""
All Concrete Handlers either handle a request or pass it to the next handler in
the chain.
"""

class ParametersScript(AbstractHandler):
    def handle(self, request: Any, parameters) -> str:
        if request == 'parameters':
            tmp_params = {x: parameters[x] for x in parameters if x not in ['learning','load','color','picture_size','optimizer']}
            input_list =[parameters['width_size'],parameters['height_size']]
            lines =['']
            for key, value in tmp_params.items():
                if '('not in value and  not isinstance(value, list) and value.isdigit() == False and value.replace(".", "", 1).isdigit()== False:
                    new_line = f'{key} = "{value}"'
                else:
                    new_line = f'{key} = {value}'
                lines.append(new_line)
            input_size = f'input_shape = [{input_list[0]}, {input_list[1]}]'
            optimizer = f'optimizer = tf.keras.optimizers.{parameters["optimizer"]}(learning_rate=learning_rate,momentum=momentum)'
            lines.append(input_size)
            lines.append(optimizer)
            text = "\n".join(lines)
            return text
        else:
            return super().handle(request,parameters)

class PrepationScript(AbstractHandler):
    def handle(self, request: Any, parameters) -> str:
        if request == 'preparation':
            file_path = ff.get_file_path('preparation')
            line =''
            if ff.get_file_path(parameters['model_name']) == 'pretrained':
                line = "\n"+ff.get_pretrained_import_line(parameters['model_name'])
            storage_file = storage.open(file_path , 'r')
            return storage_file.read().decode('ascii')+line
        else:
            return super().handle(request,parameters)

class InitializeWeightsScript(AbstractHandler):
    def handle(self, request: Any, parameters) -> str:
        if request == 'initialize_weights':
            file_path = ff.get_file_path('initialize_weights')
            storage_file = storage.open(file_path , 'r')
            return storage_file.read().decode('ascii')
        else:
            return super().handle(request,parameters)

class LoadingScript(AbstractHandler):
    def handle(self, request: Any, parameters) -> str:
        if request == 'load':
            file_path = ff.get_file_path(parameters['load_data'])
            storage_file = storage.open(file_path , 'r')
            return storage_file.read().decode('ascii')
        elif request == 'load_global':
            file_path = ff.get_file_path(parameters['load_data'])
            storage_file = storage.open(file_path , 'r')
            return storage_file.read().decode('ascii')
        else:
            return super().handle(request,parameters)

class LocalLearningScript(AbstractHandler):
    def handle(self, request: Any, parameters) -> str:
        if request == 'local_learning':
            file_path = ff.get_file_path(parameters["learning"])
            storage_file = storage.open(file_path , 'r')
            return storage_file.read().decode('ascii')
        else:
            return super().handle(request,parameters)

class ModelScript(AbstractHandler):
    def handle(self, request: Any, parameters) -> str:
        if request == 'model':
            file_path = ff.get_file_path(parameters['model_name'])
            if (file_path != 'pretrained'):
                storage_file = storage.open(file_path , 'r')
                return storage_file.read().decode('ascii')
            else:
                model = parameters['model_name']
                pretrained_lines = f"""
def define_model(input_shape,number_of_classes):
    base_model = {model}(input_shape=input_shape + [3], weights='imagenet', include_top=False) #Training with Imagenet weights\n
    # This sets the base that the layers are not trainable. If we'd want to train the layers with custom data, these two lines can be ommitted.
    for layer in base_model.layers:
        layer.trainable = False
    x = Flatten()(base_model.output) #Output obtained on vgg16 is now flattened.
    prediction = Dense(number_of_classes, activation='softmax')(x) # We have 5 classes, and so, the prediction is being done on len(folders) - 5 classes
    #Creating model object
    model = Model(inputs=base_model.input, outputs=prediction)
    return model
    """
                return pretrained_lines
        else:
            return super().handle(request,parameters)

class AggregateLocallyScript(AbstractHandler):
    def handle(self, request: Any, parameters) -> str:
        if request == 'aggregate_locally':
            file_path = ff.get_file_path(parameters['aggregate_locally'])
            storage_file = storage.open(file_path , 'r')
            return storage_file.read().decode('ascii')
        else:
            return super().handle(request,parameters)


def generate_local_model(handler: Handler, session_params) -> None:
    """
    The client code is usually suited to work with a single handler. In most
    cases, it is not even aware that the handler is part of a chain.
    """
    commands = ['preparation','model','parameters','load','local_learning']
    results = []
    for comm in  commands:
        print(f"\nClient: Who wants a {comm}?")
        result = handler.handle(comm,session_params)
        if result:
            print(f"  {result}", end="")
            results.append(result)
        else:
            print(f"  {comm} was left untouched.", end="")

    return results


def generate_initial_weights(handler: Handler, session_params) -> None:
    """
    The client code is usually suited to work with a single handler. In most
    cases, it is not even aware that the handler is part of a chain.
    """
    commands = ['preparation','model','parameters','initialize_weights']
    results = []
    for comm in  commands:
        result = handler.handle(comm,session_params)
        if result:
            results.append(result)
    return results

def generate_aggregation_script(handler: Handler, session_params) -> None:
    """
    The client code is usually suited to work with a single handler. In most
    cases, it is not even aware that the handler is part of a chain.
    """
    commands = ['preparation','model','parameters','aggregate_locally']
    results = []
    for comm in  commands:
        result = handler.handle(comm,session_params)
        if result:
            results.append(result)
    return results

def generate_global_model(handler: Handler, session_params) -> None:
    """
    The template method defines the skeleton of an algorithm.
    """
    commands = ['preparation','model','pre','parameters','load_global','local_learning']
    results = []
    for comm in  commands:
        result = handler.handle(comm,session_params)
        if result:
            results.append(result)
    return results

class ScriptsExecutor():
    @staticmethod
    def create_local_model(parameters):
        params_script = ParametersScript()
        prep_script = PrepationScript()
        initial_script = InitializeWeightsScript()
        load_script = LoadingScript()
        learning_script = LocalLearningScript()
        model_script = ModelScript()

        params_script.set_next(prep_script).set_next(initial_script).set_next(
            load_script).set_next(learning_script).set_next(model_script)

        return generate_local_model(params_script, parameters)

    @staticmethod
    def create_global_model(parameters):
        params_script = ParametersScript()
        prep_script = PrepationScript()
        initial_script = InitializeWeightsScript()
        load_script = LoadingScript()
        learning_script = LocalLearningScript()
        model_script = ModelScript()

        params_script.set_next(prep_script).set_next(initial_script).set_next(
            load_script).set_next(learning_script).set_next(model_script)

        return generate_global_model(params_script, parameters)

    @staticmethod
    def create_initial_weights(parameters):
        params_script = ParametersScript()
        prep_script = PrepationScript()
        initial_script = InitializeWeightsScript()
        load_script = LoadingScript()
        learning_script = LocalLearningScript()
        model_script = ModelScript()

        params_script.set_next(prep_script).set_next(initial_script).set_next(
            load_script).set_next(learning_script).set_next(model_script)

        return generate_initial_weights(params_script, parameters)


    @staticmethod
    def generate_aggregation_script(parameters):
        params_script = ParametersScript()
        prep_script = PrepationScript()
        initial_script = InitializeWeightsScript()
        load_script = LoadingScript()
        learning_script = LocalLearningScript()
        model_script = ModelScript()
        aggregate_script = AggregateLocallyScript()

        params_script.set_next(prep_script).set_next(initial_script).set_next(
            load_script).set_next(learning_script).set_next(model_script).set_next(aggregate_script)

        return generate_aggregation_script(params_script, parameters)



