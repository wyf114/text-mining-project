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
                    <div class="mb-3">
                        <label for="lastline" class="form-label">Enter last line of book</label>
                        <input v-model="lastline" type="" class="form-control" id="lastline" aria-describedby="lastline">
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
                    <button type="submit" class="btn btn-primary" id="submitFile" @click="preprocessBook()">Submit</button>
                </div>
            </div>
            <hr>
            <div class="my-4">
                <h1>Required Inputs</h1>
                

                <label for="selected_chap" class="form-label">Select a chapter</label><br>
                <select id="selected_chap" v-model="selected_chap" class="form-select form-select-lg mb-3" aria-label="Default select example">
                    <option v-for="(value, index) in chapters_list" :key=value :value=index>{{value}}</option>
                    <option value="0" >I</option>
                </select>
                <br>
                <button type="button" class="btn btn-primary" id="submitInput" @click="showResults()">Submit</button>
            </div>
            <hr>

            <div class="row justify-content-center">
                <div class="col-md-6">
                    <h1 class="mt-5 mb-4">Results</h1>
                    <div class="form-floating mb-5">
                        <h3 class="fs-5 mb-4">Keywords in Selected Chapter</h3>
                        <p v-for="word in key_words" :key="word">{{ word }}</p>
                    </div>
                    <div class="form-floating mb-5">
                        <h3 class="fs-5 mb-4">Recommended Chapters</h3>
                        <p v-for="chap in recommended_chapters" :key="chap">{{ chap }}</p>
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
            value: null,
            lastline: 'the critics and the answers to these objections.',
            selected_chap: 0,
            key_words: null,
            recommended_chapters: null,
            chap_folder: 'test_data/Chapters/4339',
            books_directory: 'test_data',
            filename: '4339',
            book_name: null,
            book_text: null,
            chapters_list: [],
            dir: 'test_data/Chapters2'


        }
    },

    created(){
        

    },
    methods: {
        uploadFile(){
            this.value = document.getElementById('formFile')
            print(this.value)
        },
        checkInput(){
            if(this.selected_chap != null){
                this.showResults()
            }
            else{
                alert("Please select a chapter")
            }
        },
        async preprocessBook(){
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
        async splitBook(){
            await axios.get('http://localhost:3000/splitbook', {
                params: {
                    book_name: this.book_name,
                    lastline: this.lastline
                },
                
            })
            .then(response => {
                this.chapters_list = response.data.chapters
                console.log(this.chapters_list)

            })
        },
        async showResults(){
            await axios.get('http://localhost:3000/loadmodel?selected_chap=' + this.selected_chap + '&folder=' + this.chap_folder)
            .then(response => {
                console.log("testing", response)
                this.key_words = response.data.key_words
                this.recommended_chapters = response.data.recommendation
                console.log(this.recommended_chapters)

            })
        },

    }
}
</script>

<!--###### css #####-->
<style></style>