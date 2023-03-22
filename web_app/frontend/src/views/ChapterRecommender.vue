<!--###### template #####-->
<template>
    <div class="container-fluid">

        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <h1 class="mt-4 mb-4">Chapter Recommender</h1>
                    <!-- Upload pdf file -->
                    <div class="mb-4 ">
                        <label for="formFile" class="form-label">Upload your PDF Textbook file</label>
                        <input class="form-control" type="file" id="formFile">
                    </div>


                    <!-- ##FIX THE UPLOAD FILE BUTTON WHEN FREE ONLY##
                    <div>
                        <b-form-file v-model="file1" :state="Boolean(file1)" placeholder="Choose a file or drop it here..."
                            drop-placeholder="Drop file here..."></b-form-file>
                        <div class="mt-3">Selected file: {{ file1 ? file1.name : '' }}</div>

                        <b-form-file v-model="file2" class="mt-3" plain></b-form-file>
                        <div class="mt-3">Selected file: {{ file2 ? file2.name : '' }}</div>
                    </div>
                    -->

                    <!-- Create button -->
                    <button type="button" class="btn btn-primary" id="submit">Submit</button>
                </div>
            </div>

            <div class="row justify-content-center">
                <div class="col-md-6">
                    <h1 class="mt-5 mb-4">Results</h1>
                    <div class="form-floating mb-5">
                        <p class="fs-5 mb-4">Recommended Chapters</p>
                        <p></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<!--###### script #####-->
<script>
export default {
    name: 'ChapterRecommender',
    data() {
        return {
            file1: null,
            file2: null
        }
    }
}
</script>

<!--###### css #####-->
<style></style>