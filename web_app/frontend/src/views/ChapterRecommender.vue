<!--###### template #####-->
<template>
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
                            <label for="lastline" class="form-label">Enter last line of last chapter</label>
                            <input v-model="lastline" type="" class="form-control" id="lastline"
                                aria-describedby="lastline">
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
                        <!-- original
                        <div class="p-0">
                            <button type="submit" class="btn btn-primary" id="submitFile"
                                @click="preprocessBook(); sendFile()">Upload</button>
                        </div> -->
                        <div class="p-0">
                            <button type="submit" class="btn btn-primary" id="submitFile"
                                @click="sendFile()">Upload</button>
                        </div>
                    </div>

                    <!-- User input - Chapter -->
                    <div class="row mt-4 my-4">
                        <!-- <h1 class="fs-3 p-0">Required Inputs</h1> -->
                        <div class="mt-2 p-0">
                            <label for="selected_chap" class="form-label">
                                <h4 class="fs-6">Select a chapter</h4>
                            </label><br>
                            <select id="selected_chap" v-model="selected_chap" class="form-select form-select-lg mb-3"
                                aria-label="Default select example">
                                <option v-for="(value, index) in chapters_list" :key=value :value=index>{{ value }}</option>
                            </select>
                        </div>
                        <div class="my-2 p-0">
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
                                    Bigrams
                                </label>
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
                        <p>{display summary here}</p>
                    </div>



                    <div class="form-floating mb-3">
                        <h3 class="fs-6 fw-semibold mb-4">Book Name</h3>
                        <p>{{ filename }}</p>
                        <p>{{ lastline }}</p>
                        <p>{{ cleaned_content }}</p>
                    </div>




                </div>
            </div>

        </div>
    </div>
</template>

<!--###### script #####-->
<script>

import axios from 'axios'
export default {
    name: 'ChapterRecommender',
    data() {
        return {
            // file1: null,
            // file2: null,
            // chapters_name: null,
            // test_vecs: null,
            file: null,
            filevalue: null,

            //lastline: 'the critics and the answers to these objections.',
            lastline: null,

            selected_chap: 0,
            key_words: null,
            recommended_chapters: null,

            //chap_folder: 'test_data/Chapters/5827',
            chap_folder: null,

            books_directory: 'test_data',
            dir: 'test_data/Chapters2/',
            filename: null,
            filename: '1974',
            //filename: '5827',
            book_name: null,
            book_text: null,
            chapters_list: [],
            keyword_type: null,
            error_message: null,
            cleaned_content: null,


        }
    },

    created() {


    },
    methods: {
        selectFile() {
            //this.filevalue = document.getElementById('formFile').value
            // console.log(this.filevalue)
            this.file = this.$refs.file.files[0];
        },

        async sendFile() {
            const formData = new FormData();
            formData.append('file', this.file);
            formData.append('filename', this.filename);
            formData.append('lastline', this.lastline);

            await axios.post('http://localhost:3000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
                .then(response => {
                    //this.filename = response.data.filename
                    //this.cleaned_content = response.data.cleaned_text
                    this.chapters_list = response.data.chapters
                    this.chap_folder = response.data.chap_folder
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
        async preprocessBook() {
            await axios.get('http://localhost:3000/preprocessbook', {
                params: {
                    books_directory: this.books_directory,
                    filename: this.filename,
                    lastline: this.lastline
                }
            })
                .then(response => {
                    this.book_name = response.data.book_name
                    this.chapters_list = response.data.chapters
                    console.log(response)

                })
        },
        async showResults(){
            await axios.get('http://localhost:3000/loadmodel', {
                params: {
                    selected_chap: this.selected_chap,
                    folder: this.dir + this.filename,
                    keyword_type: this.keyword_type
                }
            })
                .then(response => {
                    console.log("testing", response)
                    this.key_words = response.data.key_words
                    this.recommended_chapters = response.data.recommendation
                    console.log(this.recommended_chapters)

                    if (this.key_words.length == 0) {
                        this.error_message = 'No valid ' + this.keyword_type + ' found in selected chapter.'
                    }
                    else {
                        this.error_message = null
                    }

                })
        },

    }
}
</script>

<!--###### css #####-->
<style></style>