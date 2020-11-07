const search_btn = document.querySelector("#search_btn")
search_btn.onclick = function(){
  document.location.href ='courses/' + $("#user_input").val();
  return false;
}
