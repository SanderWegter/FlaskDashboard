function getUsers() {
    $.getJSON("/internal/users/getAllUsers", function(data) {
        var users = [];
        $.each(data, function(key, val) {
            users.push("<tr><td>" + val.username + "</td><td>" + val.name + "</td><td>" + val.email + "</td><td>" + val.group + "</td><td>" + val.lastseen + "</td><td><a href='' onclick=\"editUserAdmin('" + val.username + "')\" data-toggle='modal' data-target='#editUserModalAdmin' class='btn btn-sm btn-info'>Edit</a></td></tr>");
        });
        $(".userList").html(users);
        $("#userTable").DataTable({
            'paging': true,
            'lengthChange': true,
            'searching': true,
            'ordering': true,
            'info': true,
            'autoWidth': true,
            'language': {
                'search': "_INPUT_",
                'searchPlaceholder': "Search..."
            }
        })
    });
}

function getGroups() {
    $.getJSON("/internal/groups/getAllGroups", function(data) {
        var group = [];
        $.each(data, function(key, val) {
            var en = ""
            if (val.name == "Admins" || val.name == "Unassigned") {
                en = "disabled"
            }
            group.push("<tr><td>" + val.name + "</td><td>" + val.members + "</td><td><a href='' data-toggle='modal' data-target='#editGroupModal' class='btn btn-sm btn-info' onclick=\"editGroupAdmin()\">Edit</a>&nbsp;<a href='' class='btn btn-danger btn-sm' " + en + " onclick=\"delGroup('" + val.id + "')\">Delete</a></td></tr>");
        });
        $(".groupList").html(group);
        $("#groupTable").DataTable({
            'paging': true,
            'lengthChange': true,
            'searching': true,
            'ordering': true,
            'info': true,
            'autoWidth': false,
            'columnDefs': [
                { "width": "75px", "targets": 0 },
                { "width": "60px", "targets": 1 },
                { "width": "110px", "targets": 2 }
            ],
            'language': {
                'search': "_INPUT_",
                'searchPlaceholder': "Search..."
            }
        })
    });
}




function editUserAdmin(user) {
    $(".editUserTitle").html("Edit user " + user);
    $("#saveUser").attr("onclick", "saveUserEdit()");
    $("#saveUser").prop("disabled", true);

    $.getJSON("/internal/users/getUserInfoAdmin/" + user, function(data) {
        $.each(data, function(key, val) {
            if (key == "group") {
                $("#" + key, "#editUserModalAdmin").html("");
                $("#" + key, "#editUserModalAdmin").append("<option value='" + val + "'>" + val + "</option>");
                $.getJSON("/internal/groups/getAllGroups", function(data) {
                    $.each(data, function(k, v) {
                        if (v.name != val) {
                            $("#" + key, "#editUserModalAdmin").append("<option value='" + v.name + "'>" + v.name + "</option>");
                        }
                    })
                });
            } else {
                $("#" + key, "#editUserModalAdmin").val(val);
            }
        });
        $("#saveUser").prop("disabled", false);
    });
}

function delGroup(grid) {
    var c = confirm("Are you sure?\n\nDeleting a group is irreversible and might damage the system.");
    if (c) {
        var cc = confirm("Are you sure?\n\nDeleting a group is irreversible and might damage the system.");
        if (cc) {
            $.getJSON("/internal/groups/delGroup/" + grid, function(d) {

            });
        }
    }
}


$(document).ready(function() {
    getUsers();
    getGroups();
})