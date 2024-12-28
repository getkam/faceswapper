function selectItem(selectedImg){
  var allImages = selectedImg.parentNode.getElementsByTagName('img');
  

  Array.from(allImages).forEach(element => {
    element.classList.remove('selected-img');
  });

  selectedImg.classList.add('selected-img');

  if(selectedImg.classList.contains('target-face')){
    document.getElementById('selected_target_face').value = selectedImg.getAttribute('data-value');
  }
  if(selectedImg.classList.contains('source-face')){
    document.getElementById('selected_source_face').value = selectedImg.getAttribute('data-value');
  }
  if(selectedImg.classList.contains('biometric-face')){
    document.getElementById('selected_biometric_face').value = selectedImg.getAttribute('data-value');
  }
}

function uploadFile(element){
  element.parentNode.submit();
}

function submitSwapForm(){
  var targetFace = document.getElementById('selected_target_face').value;
  var sourceFace = document.getElementById('selected_source_face').value;

  if(targetFace == '' || sourceFace == ''){
    alert('Please select both target and source faces');
    return false;
  }

  return true;
}