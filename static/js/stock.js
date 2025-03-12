$(document).ready(function() {


    // When the Add Stock modal is shown, store the triggering button and populate modal fields.
    $('#addStockModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        // Store the button globally for later use.
        window.triggeringGroupedButton = button;
        
        // Get product details from the button's data attributes.
        var productId = button.data('product-id');
        var productName = button.data('product-name');
        
        console.log("Add Stock Modal - Product Name:", productName);
        
        var modal = $(this);
        // Set the product name in the modal header.
        modal.find('#modalProductName').text(productName);
        // Set the hidden field with product id.
        modal.find('#modalProductId').val(productId);
        // Clear the user-editable fields:
        modal.find('input[name="quantity"]').val('');
        modal.find('input[name="expiry_date"]').val('');
        modal.find('input[name="batch"]').val('');
    });

    // Handle the Add Stock form submission using AJAX.
    $('#stockForm').on('submit', function(e) {
        e.preventDefault();
        // Optionally log the serialized form data.
        console.log("Submitting Add Stock Form:", $(this).serialize());
        
        $.ajax({
            type: 'POST',
            url: addStockUrl,  // Defined in your template via {% url 'add_stock' %}
            data: $(this).serialize(),
            success: function(response) {
                if(response.success){
                    alert(response.message);
                    $('#addStockModal').modal('hide');
                    // Retrieve the button that triggered the modal.
                    var button = window.triggeringGroupedButton;
                    if (!button) {
                        console.error("Triggering button not found");
                        return;
                    }
                    // Find the closest table row and update its total quantity cell.
                    var row = button.closest('tr');
                    row.find('.total_quantity').text(response.total_quantity);
                    console.log("Updated total quantity cell with:", response.total_quantity);
                } else {
                    console.log('Validation errors:', response.errors);
                    alert('There were errors in your submission.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Add Stock AJAX error:', status, error);
                console.error('Response:', xhr.responseText);
                alert('An error occurred while adding stock: ' + error);
            }
        });
    });

    // Update Stock Detail Modal (for overwriting a PackedStock record)
    // When the detail modal is shown, populate its fields.
    $('#updateStockDetailModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        console.log("Storing triggering detail button:", button);
        window.triggeringDetailButton = button;
            
        // Get product-specific details and the record identifiers (e.g. expiry date, batch) from data attributes.
        var productId = button.data('product-id');
        var productName = button.data('product-name');
        var expiryDate = button.data('expiry-date');
        var batch = button.data('batch');
            
        console.log("Detail Modal - Product Name:", productName);
        console.log("Detail Modal - Expiry Date:", expiryDate);
        console.log("Detail Modal - Batch:", batch);
            
        var modal = $(this);
        // Set the modal header with the product name.
        modal.find('#modalProductName').text(productName);
        // Populate hidden fields in the detail modal.
        modal.find('#detailModalProductId').val(productId);
        modal.find('#detailModalExpiryDate').val(expiryDate);
        modal.find('#detailModalBatch').val(batch);
        // Clear the user-editable fields:
        modal.find('input[name="quantity"]').val('');
    });
 
    // Handle the Update Stock Detail form submission via AJAX.
    $('#stockdetailForm').on('submit', function(e) {
        e.preventDefault();
        console.log("Submitting Update Stock Detail Form:", $(this).serialize());
        $.ajax({
            type: 'POST',
            url: addStockDetailUrl,  // Defined in your template via {% url 'add_stock_detail' %}
            data: $(this).serialize(),
            success: function(response) {
                if(response.success){
                    alert(response.message);
                    $('#updateStockDetailModal').modal('hide');
                    var button = window.triggeringDetailButton;
                    if (!button) {
                        console.error("Triggering detail button not found");
                        return;
                    }
                    var row = button.closest('tr');
                    row.find('.total_quantity').text(response.total_quantity);
                    console.log("Updated detail total quantity cell with:", response.total_quantity);
                } else {
                    console.log('Validation errors:', response.errors);
                    alert('There were errors in your submission.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Detail AJAX error:', status, error);
                console.error('Response:', xhr.responseText);
                alert('An error occurred while updating stock: ' + error);
            }
        });
    });
 
    // Remove Stock Modal (for removing packed stock)
    // When the removal modal is shown, populate its hidden fields.
    $('#removeStockModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        // Store the button globally for later use.
        window.triggeringRemoveButton = button;
        var productId = button.data('product-id');
        var productName = button.data('product-name');
        
        var modal = $(this);
        modal.find('#removeModalProductName').text(productName);
        modal.find('#removeModalProductId').val(productId);
        // Clear the user-editable fields:
        modal.find('input[name="quantity"]').val('');
    });
    
    // Handle the Remove Stock form submission via AJAX.
    $('#removeStockForm').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: removeStockUrl,  // Defined in your template via {% url 'remove_stock' %}
            data: $(this).serialize(),
            success: function(response) {
                if(response.success){
                    alert(response.message);
                    $('#removeStockModal').modal('hide');
                    var button = window.triggeringRemoveButton;
                    if (!button) {
                        console.error("Triggering button not found");
                        return;
                    }
                    var row = button.closest('tr');
                    row.find('.total_quantity').text(response.total_quantity);
                    console.log("Updated removal total quantity cell with:", response.total_quantity);
                } else if(response.warning) {
                    if(confirm(response.message)){
                        $('#removeStockForm input[name="confirm"]').prop('checked', true);
                        $('#removeStockForm').submit();
                    }
                } else {
                    console.log('Validation errors:', response.errors);
                    alert('There were errors in your submission.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Remove Stock AJAX error:', status, error);
                console.error('Response:', xhr.responseText);
                alert('An error occurred while removing stock: ' + error);
            }
        });
    });


    // Add label stock
    // When the modal is shown, store the triggering button and populate modal fields.
    $('#addLabelStockModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        window.triggeringGroupedButton = button; // Store the button globally for later use.
        
        var itemName = button.attr('data-item-name');
        var itemHasTwoLabels = button.attr('data-item-has-two-labels');
        
        console.log("Label view - Item Name:", itemName);
        console.log("label_quantity_1: " + $('#id_label_quantity_1').val());
        console.log("label_quantity_2: " + $('#id_label_quantity_2').val());
        
        var modal = $(this);
        modal.find('#modalLabelName').text(itemName);
        modal.find('#labelModalItemNameHidden').val(itemName);
        modal.find('#labelModalItemHasTwoLabels').val(itemHasTwoLabels);

        // Fetch the form with the correct configuration:
        $.ajax({
            type: 'GET',
            url: fetchLabelStockFormUrl,
            data: { has_two_labels: itemHasTwoLabels },
            success: function(response) {
                // Replace the form fields area in the modal with the rendered HTML.
                modal.find('#labelFormFields').html(response.form_html);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching form:', status, error);
            }
        });
    });

    // Add label stock
    // Handle the form submission using AJAX.
    $('#labelStockForm').on('submit', function(e) {
        e.preventDefault();
        // Log the serialized form data to check what's being sent.
        console.log($(this).serialize());
        $.ajax({
            type: 'POST',
            url: addLabelStockUrl,
            data: $(this).serialize(),
            success: function(response) {
                if(response.success){
                    alert(response.message);
                    $('#addLabelStockModal').modal('hide');
                    // Retrieve the button that triggered the modal from the global variable.
                    var button = window.triggeringGroupedButton;
                    if (!button) {
                        console.error("Triggering button not found");
                        return;
                    }
                    // Find the closest table row to that button.
                    var row = button.closest('tr');
                    // Update the cell showing the total quantity.
                    row.find('.total_quantity_1').text(response.total_quantity_1);
                    row.find('.total_quantity_2').text(response.total_quantity_2);
                    console.log("Updated total quantity 1 cell with:", response.total_quantity_1);
                    console.log("Updated total quantity 2 cell with:", response.total_quantity_2);
                } else {
                    console.log('Validation errors:', response.errors);
                    alert('There were errors in your submission.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Grouped view AJAX error:', status, error);
                console.error('Response:', xhr.responseText);
                alert('An error occurred while adding stock: ' + error);
            }
        });
    });


});
