<template>
    <div id="users" class="dashboard-item bg-white shadow-md rounded-lg p-6 hidden fade-in">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6">{{ title }}</h2>
        <p>{{ message }}</p>
    </div>
</template>

<script>
export default {
    name: 'GenericComponent',
    props: {
        title: {
            type: String,
            required: true
        },
        message: {
            type: String,
            required: true
        }
    }
}
</script>