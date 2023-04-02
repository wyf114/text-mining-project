<template>
    <nav class="navbar fixed-top navbar-expand-lg">
        <div class="container-fluid">
            <!--logo-->
            <a class="navbar-brand" href="/"><img src="../assets/coursereads-logo.png" height="30"></a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav" style="background-color: white;">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link mx-3" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link mx-3" href="/text-summarizer">Text Summarizer</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link mx-3" href="/chapter-recommender">Chapter Recommender</a>
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

<style>
.navbar {
    background-color: white;
}
</style>