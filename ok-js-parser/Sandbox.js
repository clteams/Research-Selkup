function write(t) {
  document.querySelector('.posting-form_itx_dec').click();
  setTimeout(function() {
    document.querySelector('#posting_form_text_field').innerHTML=t;
    document.querySelectorAll('[type=submit]')[1].classList.remove('__disabled');
    setTimeout(function() {
      document.querySelectorAll('[type=submit')[1].click();
    }, 100);
  }, 200);
}