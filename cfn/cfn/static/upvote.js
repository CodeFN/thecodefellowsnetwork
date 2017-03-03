$('#add_comment').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    add_up_vote();
});

$('#upVote').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    add_up_vote();
});

function create_post() {
    console.log("create post is working!") // sanity check
    console.log($('#post-text').val())
};

function add_comment() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "upvote/", // the endpoint
        type : "POST", // http method

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};