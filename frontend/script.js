$(document).ready(function () {
    loadMedicines();
    loadAveragePrice();
});

function loadMedicines() {
    $.get("http://localhost:8000/medicines").done(function (data) {
        const tableBody = $("#medicineTable");
        tableBody.empty();
        data.medicines.forEach(med => {
            tableBody.append(`
                <tr>
                    <td>${med.name}</td>
                    <td>${med.price}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="openUpdateForm('${med.name}', '${med.price.replace('£', '')}')">Update</button>
                        <button class="btn btn-danger btn-sm" onclick="openDeleteModal('${med.name}')">Delete</button>
                    </td>
                </tr>
            `);
        });
    }).fail(function (xhr, status, error) {
        const response = xhr.responseJSON;
        const errorMessage = response ? response.message || response.detail : "Failed to load medicines.";
        alert(`Error: ${errorMessage}`);
    });
}

function loadAveragePrice() {
    $.get("http://localhost:8000/average_price").done(function (data) {
        $("#averagePrice").text(data.average_price);
    }).fail(function (xhr, status, error) {
        const response = xhr.responseJSON;
        const errorMessage = response ? response.message || response.detail : "Failed to load average price.";
        alert(`Error: ${errorMessage}`);
    });
}

function openUpdateForm(name, price) {
    $("#updateName").val(name);
    $("#updatePrice").val(price);
    new bootstrap.Modal(document.getElementById('updateModal')).show();
}

$("#updateForm").submit(function (e) {
    e.preventDefault();
    const name = $("#updateName").val();
    const price = parseFloat($("#updatePrice").val());
    if (price < 0) {
        alert("Price cannot be negative.");
        return;
    }
    $.ajax({
        url: "http://localhost:8000/update",
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data: { name, price },
        success: function () {
            location.reload();
        },
        error: function (xhr, status, error) {
            const response = xhr.responseJSON;
            const errorMessage = response ? response.message || response.detail : "Failed to update medicine.";
            alert(`Error: ${errorMessage}`);
        }
    });
});

function openDeleteModal(name) {
    $("#confirmDelete").data("name", name);
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}

$("#confirmDelete").click(function () {
    const name = $(this).data("name");
    $.ajax({
        url: "http://localhost:8000/delete",
        method: "DELETE",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data: { name },
        success: function () {
            location.reload();
        },
        error: function (xhr, status, error) {
            const response = xhr.responseJSON;
            const errorMessage = response ? response.message || response.detail : "Failed to delete medicine.";
            alert(`Error: ${errorMessage}`);
        }
    });
});

function openCreateForm() {
    new bootstrap.Modal(document.getElementById('createModal')).show();
}

$("#createForm").submit(function (e) {
    e.preventDefault();
    const name = $("#createName").val();
    const price = parseFloat($("#createPrice").val());
    if (price < 0) {
        alert("Price cannot be negative.");
        return;
    }
    $.ajax({
        url: "http://localhost:8000/create",
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data: { name, price },
        success: function () {
            location.reload();
        },
        error: function (xhr, status, error) {
            const response = xhr.responseJSON;
            const errorMessage = response ? response.message || response.detail : "Failed to create medicine.";
            alert(`Error: ${errorMessage}`);
        }
    });
});