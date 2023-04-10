<!--###### template #####-->
<template>
    <Loading v-show="loading" />
    <div class="container-fluid h-100">

        <div class="container my-4 py-4 h-100" id="main">
            <div class="row p-3 bg-white rounded-4">
                
                <!-- Chapter Recommender -->
                <div class="col-6 px-5">
                    <div class="row">
                        <h1 class="fs-6 fw-bold my-4 p-0">Chapter Recommender</h1>
                        <hr>
                        <!-- Upload pdf file -->
                        <div class="mb-4 p-0">
                            <label for="formFile" class="form-label">
                                Upload your book here (.txt)
                            </label>
                            <input @change="selectFile" ref="file" class="form-control" type="file" id="formFile">
                        </div>
                        <div class="mb-4 p-0">
                            <label for="firstline" class="form-label">Enter first line of first line chapter</label>
                            <input v-model="firstline" type="text" class="form-control" id="firstline"
                                aria-describedby="firstline">
                        </div>
                        <div class="mb-4 p-0">
                            
                            <label for="lastline" class="form-label">Enter last line of last chapter</label>
                            <input v-model="lastline" type="text" class="form-control" id="lastline"
                                aria-describedby="lastline">
                        </div>

                        <div class="p-0">
                            <button type="submit" class="btn btn-primary" id="submitFile"
                                @click="sendFile()">Upload</button>
                        </div>
                    </div>

                    <!-- User input - Chapter -->
                    <div v-show="chapters_list.length != 0" class="row mt-4 my-4">
                        <!-- <h1 class="fs-3 p-0">Required Inputs</h1> -->
                        <div class="mt-2 p-0">
                            <label for="selected_chap" class="form-label">
                                <h4 class="fs-6">Select a chapter</h4>
                            </label><br>
                            <select id="selected_chap" v-model="selected_chap" class="form-select form-select-lg mb-3"
                                aria-label="Default select example">
                                <option v-for="chap in chapters_list" :key=chap :value=chap>{{ chap }}</option>
                            </select>
                        </div>
                        <div class="mb-4 p-0 row my-2 p-0">
                            <div class="col-6">
                                <label for="noOfSen" class="form-label">Enter number of sentences for summary</label>
                                <input v-model="noOfSen" type="number" class="form-control" id="noOfSen"
                                    aria-describedby="noOfSen" min="1" max="5">
                            </div>
                            <div class="col-1">

                            </div>
                            <div class="col-5">
                                <h4 class="fs-6">Type of keywords </h4>
                                <div class="form-check">
                                    <input v-model="keyword_type" value='unigrams' class="form-check-input" type="radio"
                                        name="flexRadioDefault" id="flexRadioDefault1">
                                    <label class="form-check-label" for="flexRadioDefault1">
                                        Unigrams
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input v-model="keyword_type" value='bigrams' class="form-check-input" type="radio"
                                        name="flexRadioDefault" id="flexRadioDefault2" checked>
                                    <label class="form-check-label" for="flexRadioDefault2">
                                        Bigrams/Trigrams
                                    </label>
                                </div>
                            </div>
                            
                        </div>

                        <div class="mt-2 p-0">
                            <button type="button" class="btn btn-primary" id="submitInput" @click="showResults()">Generate
                                Results</button>
                        </div>
                    </div>

                </div>

                <!-- Results Column -->
                <div class="col-6 ps-4" style="border-left:1px solid lightgrey;">
                    <h1 class="fs-6 fw-bold my-4">Results</h1>
                    <hr>
                    <div class="form-floating mb-3">
                        <h3 class="fs-6 fw-semibold mb-4">Keywords</h3>
                        <p style="display: inline-block;" v-for="word in key_words" :key="word">{{ word }},&nbsp;</p>
                        <p v-if="error_message" class="text-danger">{{ error_message }}</p>
                    </div>
                    <div class="form-floating mb-3">
                        <h3 class="fs-6 fw-semibold mb-4">Recommended Chapters</h3>
                        <p class="text-break" style="display: inline-block;" v-for="chap in recommended_chapters" :key="chap">{{ chap }},&nbsp;</p>
                    </div>
                    <div class="form-floating mb-3">
                        <h3 class="fs-6 fw-semibold mb-4">Summarisation</h3>
                        <p>{{ summary }}</p>
                    </div>

                </div>
            </div>

        </div>
    </div>
</template>

<!--###### script #####-->
<script>

import axios from 'axios'
import Loading from "../components/Loading";
export default {
    name: 'ChapterRecommender',
    data() {
        return {
            file: null,
            filevalue: null,

            firstline: null,
            lastline: null,

            selected_chap: 0,
            noOfSen: 3,

            key_words: null,
            recommended_chapters: null,
            summary: null,

            chap_folder: null,

            books_directory: 'test_data',
            dir: 'test_data/Chapters/',
            filename: null,
            book_name: null,
            book_text: null,
            chapters_list: [],
            keyword_type: 'bigrams',
            error_message: null,
            cleaned_content: null,
            loading: false
        }
    },

    components: {Loading},

    created() {


    },
    methods: {
        selectFile() {
            this.file = this.$refs.file.files[0];
            this.chapters_list = []
            this.error_message = null
            this.recommended_chapters = null
            this.lastline = null
            this.key_words = null,
            this.summary = null
        },

        async sendFile() {
            this.loading = true
            const formData = new FormData();
            formData.append('file', this.file);
            formData.append('filename', this.filename);
            formData.append('firstline', this.firstline);
            formData.append('lastline', this.lastline);

            await axios.post('http://localhost:3000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
                .then(response => {
                    this.chapters_list = response.data.chapters
                    this.chap_folder = response.data.chap_folder
                    this.loading = false
                })
        },

        checkInput() {
            if (this.selected_chap != null) {
                this.showResults()
            }
            else {
                alert("Please select a chapter")
            }
        },
        
        async showResults(){
            this.loading = true
            await axios.get('http://localhost:3000/loadmodel', {
                params: {
                    selected_chap: this.selected_chap,
                    folder: this.chap_folder,
                    keyword_type: this.keyword_type,
                    number_of_sentences: this.noOfSen
                }
            })
                .then(response => {
                    console.log("testing", response)
                    this.key_words = response.data.key_words
                    this.recommended_chapters = response.data.recommendation
                    this.summary = response.data.summary
                    console.log(this.recommended_chapters)

                    if (this.key_words.length == 0) {
                        this.error_message = 'No valid ' + this.keyword_type + ' found in selected chapter.'
                    }
                    else {
                        this.error_message = null
                    }
                    this.loading = false

                })
        },

    }
}
</script>

<!--###### css #####-->
<style></style>