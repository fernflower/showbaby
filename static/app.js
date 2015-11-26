$('.submitbtn').click(function (){$.post('/manage', 'button=' + this.id, function (data) {
    if (data['result'] == 'fail') {
        $('#result').text(data['error']);
    };
    location.reload();
})});
