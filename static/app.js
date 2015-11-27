$('.submitbtn').click(function (){$.ajax({
    type: 'POST',
    url: '/manage',
    dataType: 'json',
    data: {'button': this.id},
    success: function (data) {
        if (data['result'] == 'fail') {
            $('#result').text(data['error']);
        };
        location.reload();},
  });
});
