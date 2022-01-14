


<script>
import { Bar } from "vue3-chart-v2";

export default {
  name: 'ChartResult',
  extends: Bar,
  props: {
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      required: false
    }
  },
  mounted() {
    console.log("hello")
    this.renderChart(this.chartData, this.chartOptions);
  },
};
</script>
