class User {
    constructor() {
        // maping important html elements by id
        this.userListTable = $('table');
        this.addUserForm = $('#addUserForm');
        this.editUserForm = $('#editUserForm');
        this.deleteUserForm = $('#deleteUserForm');
        this.addUserForm_is_child = $('#addUserForm-is_child');
        this.editUserForm_is_child = $('#editUserForm-is_child');
        this.addUserForm_parent = $('#addUserForm .parent');
        this.addUserForm_address = $('#addUserForm .address');
        this.editUserForm_parent = $('#editUserForm .parent');
        this.editUserForm_address = $('#editUserForm .address');
        this.users = []
        // important api endpoints of user CRUD
        this.apiUser = '/api/v1/users/';
    }

    // check is_child checkbox checked or not. Depending on that do necessary actions
    checkIsChildCheckedOrNot = () => {
        let self = this;
        // In user add form if user is child then user does not need to input address but need to select parent
        self.addUserForm_is_child.on('click', function (e) {
            self.addUserForm_parent.toggle('hidden');
            self.addUserForm_address.toggle('hidden');
        });

        // In user edit form if user is child then user does not need to input address but need to select parent
        self.editUserForm_is_child.on('click', function (e) {
            self.editUserForm_parent.toggle('hidden');
            self.editUserForm_address.toggle('hidden');
        });
    }

    // call user list api and show list of users in user table
    allUsers = () => {
        let self = this
        let tableData = ``;
        let selectOption = `<option selected disabled>Select Parent</option>`;

        $.ajax({
            url: self.apiUser,
            method: 'GET',
            success: function (data) {
                self.users = data;
                self.users.map(function (value, index) {
                    tableData += `            
                    <tr>
                        <th scope="row">${index + 1}</th>
                        <td>${value.first_name}</td>
                        <td>${value.last_name}</td>
                        <td>${value.address}</td>
                        <td>
                            <i class="fas fa-user-edit user-edit" data-toggle="modal" data-target="#userEditModal" data-userId="${value.id}"></i>  
                            <i class="fas fa-user-times user-delete" data-toggle="modal" data-target="#userDeleteModal" data-userId="${value.id}"></i>
                        </td>
                    </tr>`;

                    selectOption += `<option value='${value.id}'>${value.first_name} ${value.last_name}</option>`;
                });

                // if no user found then show proper message
                if (data.length == 0) {
                    tableData = '<td class="text-center" colspan="5">No user found</td>'
                }
                self.userListTable.find('tbody').html(tableData);
                self.addUserForm_parent.html(selectOption);
                self.editUserForm_parent.html(selectOption);


            },
            error: function (request, error) {

            }
        });
    }

    // set user information in UserEditModal. 
    setUserInformationOnEditUserModal = userId => {
        let self = this;
        // get specific user from list of users
        var user = self.users.filter(function (user) {
            return user.id == userId;
        })[0];

        // set user information in editUserModal form
        self.editUserForm.find("input[name='last_name']").first().focus();
        self.editUserForm.find("input[name='first_name']").val(user.first_name);
        self.editUserForm.find("input[name='last_name']").val(user.last_name);
        self.editUserForm.find("input[name='street']").val(user.street);
        self.editUserForm.find("input[name='city']").val(user.city);
        self.editUserForm.find("input[name='state']").val(user.state);
        self.editUserForm.find("input[name='zip']").val(user.zip);

        // reset checkbox as unchecked
        if (self.editUserForm.find("input[name='is_child']").is(':checked')) {
            self.editUserForm.find("input[name='is_child']").click();
            self.editUserForm.find("select[name='parent']").prop('selectedIndex', 0);
        };

        // if user is child then it has parent & no address
        if (user.is_child) {
            self.editUserForm.find("input[name='is_child']").click();
            self.editUserForm.find("select[name='parent']").val([user.parent]);
        }

        // can't select itself as parent
        $("#editUserForm option").attr("disabled", false);
        $("#editUserForm option:first-child").attr("disabled", true);
        $("#editUserForm option[value='" + userId + "'").attr("disabled", true);
    }

    // add a new user after successfull submission of addUserFrom
    userAdd = () => {
        let self = this;
        self.addUserForm.on('submit', function (e) {
            e.preventDefault();
            var data = {}
            data.first_name = $(this).find("input[name='first_name']").val();
            data.last_name = $(this).find("input[name='last_name']").val();
            data.is_child = ($(this).find("input[name='is_child']").is(':checked')) == true ? 1 : 0;
            if (data.is_child) {
                data.parent = $(this).find("select[name='parent']").val();
                if (data.parent == null) {
                    self.addUserForm_parent.css('border-color', 'red');
                    self.addUserForm_parent.on('change', function (e) {
                        self.addUserForm_parent.css('border-color', '#ced4da');
                    })
                    return;
                }

            } else {
                data.street = $(this).find("input[name='street']").val();
                data.city = $(this).find("input[name='city']").val();
                data.state = $(this).find("input[name='state']").val();
                data.zip = $(this).find("input[name='zip']").val();
            }

            $.ajax({
                url: self.apiUser,
                method: 'POST',
                data: data,
                dataType: "json",
                success: function (data) {
                    $.notify("A new user added successfully", "success");
                    $('#userAddModal').modal('toggle');
                    self.allUsers();
                },
                error: function (request, error) {
                    $.notify("Something went wrong. " + error);
                }
            });
        });
    }

    // edit existing user information after successfull submission of editUserFrom
    userEdit = userId => {
        let self = this;
        self.editUserForm.unbind('submit');
        self.editUserForm.on('submit', function (e) {
            e.preventDefault();

            var data = {}
            data.first_name = $(this).find("input[name='first_name']").val();
            data.last_name = $(this).find("input[name='last_name']").val();
            data.is_child = ($(this).find("input[name='is_child']").is(':checked')) == true ? 1 : 0;
            if (data.is_child) {
                // if user is child then user must have a parent
                data.parent = $(this).find("select[name='parent']").val();
                if (data.parent == null) {
                    self.editUserForm_parent.css('border-color', 'red');
                    self.editUserForm_parent.on('change', function (e) {
                        self.editUserForm_parent.css('border-color', '#ced4da');
                    })
                    return;
                }

            } else {
                data.street = $(this).find("input[name='street']").val();
                data.city = $(this).find("input[name='city']").val();
                data.state = $(this).find("input[name='state']").val();
                data.zip = $(this).find("input[name='zip']").val();
            }
            // apachi super set, microsoft power bi
            $.ajax({
                url: self.apiUser + userId + '/',
                method: 'PATCH',
                data: data,
                cache: false,
                dataType: "json",
                success: function (data) {
                    $.notify("User information updated successfully", "success");
                    $('.modal-header .close').click();
                    self.allUsers();
                },
                error: function (request, error) {
                    $.notify("Something went wrong. " + error);
                }
            });
        });
    }

    // delete an existing user after successfull submission of deleteUserForm
    userDelete = userId => {
        console.log(userId)
        let self = this;
        self.deleteUserForm.unbind('submit');
        self.deleteUserForm.on('submit', function (e) {
            e.preventDefault();
            $.ajax({
                url: self.apiUser + userId + '/',
                method: 'DELETE',
                success: function (data) {
                    $.notify("User deleted successfully", "success");
                    $('.modal-header .close').click();
                    self.allUsers();
                },
                error: function (request, error) {
                    $.notify("Something went wrong. " + error);
                }
            });
        });
    }
}

// creating a new user instance
let user = new User();

// get and set all users in user table
user.allUsers();

// action on click is_child checkbox
user.checkIsChildCheckedOrNot();

// action on user-add icon
user.userAdd();

// action on user-edit icon
$(document).on('click', '.user-edit', function (e) {
    user.setUserInformationOnEditUserModal($(this).data('userid'));
    user.userEdit($(this).data('userid'));
});

// action on user-delete icon
$(document).on('click', '.user-delete', function (e) {
    console.log($(this).data('userid'));
    user.userDelete($(this).data('userid'));
});


