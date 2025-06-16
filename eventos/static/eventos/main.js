$(function(){
  const endpoint = $('#eventos-container').data('url');

  $('#buscador').on('keyup', function(){
    clearTimeout(window.searchDelay);
    const q = $(this).val();
    window.searchDelay = setTimeout(function(){
      $.get(endpoint, { q }, function(data) {
        $('#resultados').html(data.html);
      });
    }, 300);
  });
});
