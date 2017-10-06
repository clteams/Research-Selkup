var DOMProfileI = document.getElementsByClassName('user-profile_i');
var ProfileInfo = new Object();

if (DOMProfileI.length > 0) {
  for (var i = 0; i < DOMProfileI.length; i ++) {
     var localEllip = DOMProfileI[i].getElementsByClassName('ellip');
     if (localEllip.length == 0) continue;
     var localTico = localEllip[0].getElementsByClassName('tico');
     var localKey = localTico[0].getElementsByTagName('span')[0];
     var localKey = localKey.innerText;
     var localValue = localEllip[1].innerText;
     ProfileInfo[localKey] = localValue;
  }
}
