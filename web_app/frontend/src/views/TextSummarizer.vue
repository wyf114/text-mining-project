<!--###### template #####-->
<template>
    <div class="container-fluid">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <h1 class="mt-4 mb-4">Text Summarizer</h1>
                    <p>Enter your paragraph here:</p>
                    <div class="form-floating mb-4">
                        <textarea class="form-control" placeholder="Leave a comment here" id="floatingTextarea2"
                            style="height: 100px"></textarea>
                        <label for="floatingTextarea2" class="text-secondary">Paste a paragraph here to summarize!</label>
                    </div>
                    <!-- Create button -->
                    <button type="button" class="btn btn-primary" id="submit">Submit</button>
                </div>
            </div>

            <!-- Display textbox as results -->
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <h1 class="mt-5 mb-4">Results</h1>
                    <div class="form-floating mb-5">
                        <p class="fs-5 mb-4">Keywords: Display results here</p>

                        <p class="fs-5">Summary</p>
                        <p>Display results here</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<!--###### script #####-->
<script>
export default {
    name: 'TextSummarizer'
}
</script>

<!--###### css #####-->
<style></style>