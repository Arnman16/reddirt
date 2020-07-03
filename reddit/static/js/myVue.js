postApp = new Vue({
    el: '#postApp',
    delimiters: ["<%", "%>"],
    vuetify: new Vuetify(),
    props: {
        source: String,
    },
    data: () => ({
        drawer: false,
        popup: false,
        success_alert: false,
        error_alert: false,
        postList: null,
        postListData: null,
        title: '',
        vote_color: 'red',
        url: '/api/posts/?format=json&subreddit=2',
        description: '',
        id: '',
        full_url: '',
        postDetail: false,
        postDetailData: '',
        submit_title: '',
        submit_description: '',
        postDetailTitle: '',
        postDetailDescription: '',
        detail_id: null,
        submit_user: '',
        subreddit_url: '',
        submit_subreddit: '',
        subreddit_name: '',
        select: null,
        subreddit_id: '',
        posts_loading: false,
        allPosts: '',
        postIdList: '',
        votesList: '',
        index: '',
        detail_index: null,
        edit_post_popup: false,
        upvote_style: {
            color: "orange",
        },
        downvote_style: {
            color: "blue",
        },
        novote_style: {
            color: "grey",
        },


    }),
    methods: {
        loadJson: function (url, subreddit_name, subreddit_url, subreddit_id) {
            document.body.scrollTop = 0; // For Safari
            document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
            this.drawer = false;
            this.posts_loading = true;
            this.postList = null;
            this.subreddit_id = subreddit_id;
            this.subreddit_name = subreddit_name;
            this.subreddit_url = subreddit_url;
            this.postListData = axios
                .get(url)
                .then(response => {
                    return response.data
                })
                .catch(error => {
                    console.log(error)
                })
                .finally(() => this.loading = false)
            if (this.postListData) {
            }
            // this.showPosts();
        },
        showPosts: async function () {
            if (this.postListData) {
                this.postList = await this.postListData;
                var user_id = document.getElementById("userId").value;
                window.history.pushState("object or string", "Title", this.subreddit_url);
                this.postIdList = '';
                this.posts_loading = false;
                for (post in this.postList) {
                    this.postIdList = this.postIdList.concat(this.postList[post]['id'] + ',')
                    // this.get_votes(user_id, this.postList[post]['id']);
                }
                this.get_votes();
            }
        },
        checkOrLoadSub() {
            if (this.postList == null) {
                this.showPosts();
            }
        },
        loadDetailJsonDirect: async function (url) {
            this.detail_index = 1;
            jsonurl = '/api/allposts/' + url;
            this.postDetailData = await axios
                .get(jsonurl)
                .then(response => {
                    return response.data;
                })
                .catch(error => {
                    console.log(error);
                    this.error_alert = !this.error_alert;
                })
                .finally(() => this.loading = false);
                if (this.postDetailData != '') {
                    this.postDetail = !this.postDetail;
                    this.postDetailTitle = await this.postDetailData['title']
                    this.postDetailDescription = await this.postDetailData['description']
                    this.detail_id = await this.postDetailData['id']
                    this.get_votes_detail_direct()
                }
        },
        loadDetailJson: async function (index) {
            this.detail_index = index;
            // jsonurl = '/api/allposts/' + url;
            this.postDetailData = this.postList[index];
            // this.detail_id = this.postList[index]['id'];
            // this.postDetailData = await axios
            //     .get(jsonurl)
            //     .then(response => {
            //         return response.data;
            //     })
            //     .catch(error => {
            //         console.log(error);
            //         this.error_alert = !this.error_alert;
            //     })
            //     .finally(() => this.loading = false);
            if (this.postDetailData != '') {
                this.postDetail = !this.postDetail;
                this.postDetailTitle = await this.postDetailData['title']
                this.postDetailDescription = await this.postDetailData['description']
                this.detail_id = await this.postDetailData['id']
            }
            window.history.pushState("object or string", "Title", this.postDetailData.full_url);
        },
        submit: async function () {
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            var success_bool = await axios.post('/api/posts/', {
                title: this.submit_title,
                description: this.submit_description,
                owner: document.getElementById("userId").value,
                subreddit: this.subreddit_id,
            })
                .then(function (response) {
                    console.log(response);
                    return true;
                })
                .catch(function (error) {
                    console.log(error);
                    return false;

                });
            if (success_bool) {
                this.popup = !this.popup;
                this.success_alert = !this.success_alert;
            }
            else {
                this.popup = !this.popup;
                this.error_alert = !this.error_alert;
            }
        },
        edit_post: async function () {
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            drf_url = '/api/posts/' + this.detail_id + '/';
            var success_bool = await axios.put(drf_url, {
                title: this.postDetailTitle,
                description: this.postDetailDescription,
                owner: document.getElementById("userId").value,
                subreddit: this.subreddit_id,
            })
                .then(function (response) {
                    console.log(response);
                    return true;
                })
                .catch(function (error) {
                    console.log(error);
                    return false;

                });
            if (success_bool) {
                this.edit_post_popup = false
                this.success_alert = true;
                this.postDetailData['title'] = this.postDetailTitle;
                this.postDetailData['description'] = this.postDetailDescription;
                this.postDetailData['description_br'] = 
                    await axios
                    .get(drf_url)
                    .then(response => {
                        return response.data['description_br'];
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => this.loading = false);
            }
            else {
                this.edit_post_popup = false
                this.error_alert = true;
            }
        },
        clear() {
            this.submit_title = ''
            this.submit_description = ''
            console.log(document.getElementById("userId").value);
        },
        close_post() {
            this.checkOrLoadSub();
            window.history.pushState("object or string", "Title", '/r/' + this.postDetailData.subreddit_slug);
            this.postDetail = false;
            this.postDetailTitle = '';
            this.detail_index = null;
        },
        stringy(s1, s2) {
            return s1 + '-' + s2;
        },
        mark_votes: async function () {
            var user_id = document.getElementById("userId").value;
            postList = this.allPosts;
            console.log(postList);
        },
        get_votes_detail_direct: async function (){
            
            var voteData = await this.get_vote_promise();
                if (voteData) {
                    console.log(voteData)
                    if(voteData[0]['vote'] == 1) {
                        this.postDetailData['user_up_style'] = this.upvote_style;
                        this.postDetailData['user_down_style'] = this.novote_style;
                    }
                    else if(voteData[0]['vote'] == -1) {
                        this.postDetailData['user_up_style'] = this.novote_style;
                        this.postDetailData['user_down_style'] = this.downvote_style;
                    }
                    else {
                        this.postDetailData['user_up_style'] = this.novote_style;
                        this.postDetailData['user_down_style'] = this.novote_style;
                    }
                }
        },
        get_vote_promise: function () {
            getvotejson = '/api/post_votes/?postid_in=' + this.postDetailData.id;
            return axios
            .get(getvotejson)
            .then(response => {
                return response.data;
            })
            .catch(error => {
                console.log(error);
            })
            .finally(() => this.loading = false);
        },
        get_votes: async function () {
            const votes = await this.get_votes_promise();
            var v = 0;
            for(i in this.postList) {
                if (this.postList[i]['id'] == this.votesList[v]['post_id']) {
                    this.postList[i]['user_vote'] = this.votesList[v]['vote'];
                    if(this.votesList[v]['vote'] == 1) {
                        this.postList[i]['user_up_style'] = this.upvote_style;
                        this.postList[i]['user_down_style'] = this.novote_style;
                    }
                    else if(this.votesList[v]['vote'] == -1) {
                        this.postList[i]['user_up_style'] = this.novote_style;
                        this.postList[i]['user_down_style'] = this.downvote_style;
                    }
                    v++;
                }
                else {
                    this.postList[i]['user_up_style'] = this.novote_style;
                    this.postList[i]['user_down_style'] = this.novote_style;
                }
            }
            console.log(votes)
        },
        get_votes_promise: function () {
            getvotejson = '/api/post_votes/?postid_in=' + this.postIdList;
            return axios
                .get(getvotejson)
                .then(response => {
                    this.votesList = response.data
                    return response.data;
                })
                .catch(error => {
                    console.log(error);
                })
                .finally(() => this.loading = false);

        },
        post_vote: async function (user_id, post_id, vote, index) {
            if (this.detail_index) {
                this.index = this.detail_index;
            }
            else {
                this.index = index;
            }

            inc = vote
            getvotejson = '/api/post_votes/?postid_in=' + post_id;
            value = await axios
                .get(getvotejson)
                .then(response => {
                    return response.data;
                })
                .catch(error => {
                    console.log(error);
                })
                .finally(() => this.loading = false);
            if (value.length == 0) {
                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
                var success_bool = await axios.post('/api/post_votes/', {
                    user_id: user_id,
                    post_id: post_id,
                    vote: vote,
                })
                    .then(function (response) {
                        console.log(response);
                        return true;
                    })
                    .catch(function (error) {
                        console.log(error);
                        return false;

                    });
                if (success_bool) {
                    console.log('POST SUCCESS')
                }
                else {
                    this.error_alert = !this.error_alert;
                    console.log('POST SUCCESS')
                }
            }
            else {
                id = value[0]['id']
                if (vote == value[0]['vote']) {
                    inc = inc * -1;
                    vote = 0;
                }
                console.log(value)
                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
                puturl = '/api/post_votes/' + id + '/';
                var success_bool = await axios.put(puturl, {
                    id: id,
                    user_id: user_id,
                    post_id: post_id,
                    vote: vote,
                })
                    .then(function (response) {
                        return true;
                    })
                    .catch(function (error) {
                        console.log(error);
                        return false;

                    });
                if (success_bool) {
                    console.log('PUT SUCCESS')
                }
                else {
                    this.error_alert = !this.error_alert;
                    console.log('PUT FAIL')
                }
            }
            console.log(post_id)
            console.log(vote)
            if(vote == 1) {
                if(this.postList) {
                    this.postList[index]['user_up_style'] = this.upvote_style;
                    this.postList[index]['user_down_style'] = this.novote_style;
                }
                if(this.postDetail) {
                    this.postDetailData['user_up_style'] = this.upvote_style;
                    this.postDetailData['user_down_style'] = this.novote_style;
                }
            }
            else if(vote == -1) {
                if(this.postList) {
                    this.postList[index]['user_up_style'] = this.novote_style;
                    this.postList[index]['user_down_style'] = this.downvote_style;
                }
                if(this.postDetail) {
                    this.postDetailData['user_up_style'] = this.novote_style;
                    this.postDetailData['user_down_style'] = this.downvote_style;
                }
            }
            else {
                if(this.postList) {
                    this.postList[index]['user_up_style'] = this.novote_style;
                    this.postList[index]['user_down_style'] = this.novote_style;
                }
                if(this.postDetail) {
                    this.postDetailData['user_up_style'] = this.novote_style;
                    this.postDetailData['user_down_style'] = this.novote_style;
                }
            }
            getScoreUrl = '/api/allposts/' + post_id
            newScore = await axios
                .get(getScoreUrl)
                .then(response => {
                    return response.data['score'];
                })
                .catch(error => {
                    console.log(error);
                })
                .finally(() => this.loading = false);
            // $('#score-'+post_id).text(newScore);
            if(this.postDetailData) {
                this.postDetailData['score'] = newScore;
            }
            if(this.postList) {
                this.postList[this.index]['score'] = newScore;
            }

        }
    }

})

