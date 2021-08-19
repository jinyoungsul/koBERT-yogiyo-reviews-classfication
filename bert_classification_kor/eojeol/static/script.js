$(function() {
    $('button#evaluate').on('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_evaluate_helper', {
            evaluate_data: $('#evaluate-data').val()
        }, function (data) {
        $("#senti-result").prepend(data.result);
        $("#evaluate-input").show();
        $("#evaluate-data").val("");
      });
      return false;
    });
});

$('#evaluate_csv').on('click', function () {
    var url = $('#fileForm').attr('action');
    var form_data = new FormData();
    console.log($('#file').prop('files')[0]);
    form_data.append('file', $('#file').prop('files')[0]);

    $.ajax({
        type: 'POST',
        url: url,
        data: form_data,
        contentType: false,
        processData: false,
        success: function (data) {
            $("#csv-result").prepend(data.result);
        }
    });
});

$('textarea').each(function () {
    this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
}).on('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});


$('a#toggle-history').on('click', function () {
    var hist_toggle = $('#toggle-history');
    hist_toggle.text() === "(hide)" ? hist_toggle.text("(show)") : hist_toggle.text("(hide)");
    $("#history").toggle();
});
