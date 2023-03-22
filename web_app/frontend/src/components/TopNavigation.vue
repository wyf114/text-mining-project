<template>
    <nav class="navbar fixed-top navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <!--logo-->
            <a class="navbar-brand" href="/"><img src="../assets/logo.png" height="50" width="50"></a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link mx-3" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link mx-3" href="/text-summarizer">Text Summarizer</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link mx-3" href="/contact">Book Summarizer</a>
                    </li>
                </ul>

            </div>

        </div>
    </nav>
</template>

<script>
export default {
    name: 'TopNavigation'
}
</script>

<style></style>