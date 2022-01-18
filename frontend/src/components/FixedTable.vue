<template>
   <div>
        <h5> <strong> Common Parameters </strong> </h5>
        <table class="table table-bordered table-hover">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Value</th>
                    <th scope="col">Default value</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(parameter, index) in parameters" :key="parameter">
                    <th scope="row">{{index}}</th>
                    <td>{{parameter.name}}
                    </td>
                    <td><input v-if="isSelect(parameter.name)== false" type="number" :disabled="parameter.Selected"
                    :value="parameter.Selected ? parameter.defaultVal : parameter.value"
                    :min="getMin(parameter.name)"
                    :max="getMax(parameter.name)"
                    :step="getStep(parameter.name)" />
                    <!-- <span  v-else-if="parameter.name === 'input_size'" > -->


                    <!-- <td><input  id="inputWidth" type="number" :disabled="parameter.Selected"
                    :value="parameter.Selected ? parameter.defaultVal : parameter.value"
                    :min="getMin(parameter.name)"
                    :max="getMax(parameter.name)"
                    :step="getStep(parameter.name)" /></td>

                    <td><input  id="inputHeight"  type="number" :disabled="parameter.Selected"
                    :value="parameter.Selected ? parameter.defaultVal : parameter.value"
                    :min="getMin(parameter.name)"
                    :max="getMax(parameter.name)"
                    :step="getStep(parameter.name)" /> </td>
                        </span> -->

                    <select  :disabled="parameter.Selected" v-else>
                        <option v-for="item in parameter.value" :key="item" :selected="parameter.Selected == true && item == parameter.defaultVal">{{item}}</option>
                        </select>
                    </td>
                    <td><input type="checkbox"  v-model="parameter.Selected" /></td>
                </tr>
            </tbody>
        </table>
   </div>

</template>
<script >
export default {
  data () {
    return {
        hover: false,
        dictonaries:[],
        responses:{},
        parameters:[
         {
            name:'number_of_epochs',
            value:5,
            defaultVal: 10,
            Selected: false
        },
        {
            name:'loss_function',
            value:["categorical_crossentropy",
            "sparse_categorical_crossentropy",
            "binary_crossentropy"],
            defaultVal: "categorical_crossentropy",
            Selected: false
        },
        {
            name:'optimizer',
            value:["SGD",
            "RMSprop",
            "Adam",
            "Adadelta",
            "Adagra"
            ],
            defaultVal: "SGD",
            Selected: false
        },
        {
            name:'batch_size',
            value: 32,
            defaultVal: 32,
            Selected: false


        },
        {
            name:'validation_split',
            value: 0.2,
            defaultVal: 0.2,
            Selected: false

        },
        {
            name:'width_size',
            value:32,
            defaultVal: 32,
            Selected: false

        },
        {
            name:'height_size',
            value:32,
            defaultVal: 32,
            Selected: false

        }



        ]
    }
  },
  methods: {
    getMax(name)
    {
        switch(name){
            case 'validation_split':
                return 0.4
            case 'batch_size':
                return 128
            case 'number_of_epochs':
                return 100
            case 'input_size':
                return 224
            default:
                return 128

        }
    },
    getMin(name)
    {
        switch(name){
            case 'validation_split':
                return 0.1
            case 'batch_size':
                return 32
            case 'number_of_epochs':
                return 5
            case 'input_size':
                return 32
            default:
                return 2

        }
    },
    getStep(name)
    {
        switch(name){
            case 'validation_split':
                return 0.05
            default:
                return 1

        }

    },
    isSelect(name){
        if(['loss_function', 'optimizer', 'metric'].includes(name))
        {
            return true
        }
        return false
    },
    addRow(){
    //    this.users.push({name:'',email:'',mobno:''})
    },
    deleteRow(index){
        // this.users.splice(index,1);
    }
   }
}

</script>
