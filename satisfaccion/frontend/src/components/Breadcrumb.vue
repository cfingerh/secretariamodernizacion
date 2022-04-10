<template>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="/">Inicio</a></li>
                        <li class="breadcrumb-item" v-if="nombreAnterior"><router-link :to="urlAnterior">{{nombreAnterior}}</router-link></li>
                        <li class="breadcrumb-item active" aria-current="page">{{nombreActual}}</li>
                    </ol>
                </nav>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'Breadcrumb',
    props: ['nombreAnterior', 'urlAnterior', 'nombreActual'],
    data () {
        return {
        }
    }
}
</script>
