function editUser(){
	$(".editUserTitle").html("Edit user");
	$("#saveUser").attr("onclick","saveUserEdit()");
	$("#saveUser").prop("disabled",true);
	$.getJSON("/internal/users/getUserInfo", function(data){
		$.each(data, function(key, val){
			$("#ed"+key, "#editUserModal").val(val);
		});
		$("#saveUser").prop("disabled",false);
	});
}
function saveUserEdit(){
	var data = {
		"password": $("#edpassword", "#editUserModal").val(),
		"page": window.location.pathname
	}
	$.ajax({
		type: "POST",
		url: "/internal/users/saveUserPassword",
		data: data
	});
}

$(document).ready(function() {
});