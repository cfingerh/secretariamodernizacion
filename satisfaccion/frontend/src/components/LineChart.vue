<script>
// import { Line, mixins } from 'vue-chartjs'
import { Line } from 'vue-chartjs'
// const { reactiveProp } = mixins

export default {
    extends: Line,
    name: 'LineChart',
    // mixins: [reactiveProp],
    props: ['options', 'chartdata'],
    mounted () {
        this.renderChart(this.chartdata, this.options)
    }
}
</script>
