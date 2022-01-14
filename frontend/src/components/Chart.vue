<template>
  <div class="app">
    <apexcharts width="550" type="bar" :options="chartOptions" :series="series"></apexcharts>
    <div>
  </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'
import axios from 'axios'
export default {
  name: 'Chart',
  components: {
    apexcharts: VueApexCharts,
  },
  data: function() {
      return {
        participants:[],
        chartOptions: {
          chart: {
            id: 'vuechart-example',
            zoom: {
                enabled: true,
                type: 'x',
                resetIcon: {
                offsetX: -2,
                offsetY: 0,
                fillColor: '#f1f',
                strokeColor: '#37474F'
            },
            selection: {
                background: '#90CAF9',
                border: '#0D47A1'
            }
            }
          },
          labels: [],
                    xaxis: {
                    type: 'String'
                    }
        },
        series: [{
          name: 'accuracy',
          data: []
        }],

      }
    },
    mounted()
    {
        axios.get('/api/v1/results-for-chart/' + this.$route.params.id)
            .then(response => {
                this.participants= response.data
                console.log(this.participants['names'])
                 this.series = [{
                    name: 'accuracy',
                    data: this.participants['accuracy']
                    }]
                this.chartOptions = [{
                    chart: {
            id: 'vuechart-example',
            zoom: {
                enabled: true,
                type: 'x',
                resetIcon: {
                offsetX: -2,
                offsetY: 0,
                fillColor: '#f1f',
                strokeColor: '#37474F'
            },
            selection: {
                background: '#90CAF9',
                border: '#0D47A1'
            }
            }
          },
                    labels: this.participants['names'],
                    xaxis: {
                    type: 'String'
                    }
                }]


                console.log(this.participants)
            }).catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                } else if (error.message) {
                    this.errors.push('Something went wrong. Please try again.')
                }
            })
        this.updateChart()
    },
    methods: {
      updateChart() {
        const max = 90;
        const min = 20;
        const newData = this.series[0].data.map(() => {
          return Math.floor(Math.random() * (max - min + 1)) + min
        })
        // In the same way, update the series option
        this.series = [{
          data: this.participants['accuracy']
        }]
        this.xaxis = [{
            categories: this.participants['names']
        }]
      }
    }
}
</script>
<style scoped>
  button {
    background: #26E6A4;
    border: 0;
    font-size: 16px;
    color: '#fff';
    padding: 10px;
    margin-left: 28px;
  }
</style>

