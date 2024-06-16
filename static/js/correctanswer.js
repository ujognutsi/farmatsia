var button = document.getElementById('correctbutton');

button.addEventListener('click', function() {
  if (button.innerHTML === 'Correct!') {
    button.innerHTML = 'Incorrect!';
    button.id = 'incorrectbutton';
    var p = document.createElement('p');
    p.id = "correctp"
    p.innerHTML = 'The answer is marked as correct';
    button.parentNode.parentNode.appendChild(p);
  } 
  else {
    button.innerHTML = 'Correct!';
    button.id = 'correctbutton';
    var p = button.parentNode.querySelector('#correctp');
    if (p) {
      p.parentNode.parentNode.removeChild(p);
    }
  }
});