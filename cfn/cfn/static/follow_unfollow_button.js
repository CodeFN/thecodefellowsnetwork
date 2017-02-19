$(document).ready(function(){
    $('#follow-button').on("click", function(e){
        
        $('#follow-button').hide();
        $('#unfollow-button').show();
        console.log('before show');
        console.log('after show');
        
        e.preventDefault();
        $.ajax({
            success: function(){
                console.log("clicked");
            }
        });
    });
    $('#unfollow-button').on("click", function(e){
        
        $('#unfollow-button').hide();
        $('#follow-button').show();
        console.log('before show');
        console.log('after show');
        
        e.preventDefault();
        $.ajax({
            success: function(){
                console.log("clicked");
            }
        });
    });
});