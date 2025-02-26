// Add stock
$(document).ready(function() {
    // Handle the form submission using AJAX
    $('#stockForm').on('submit', function(e) {
        console.log("AJAX submit triggered");
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: addStockUrl,
            data: $(this).serialize(),
            success: function(response) {
                if(response.success){
                    alert(response.message);
                    $('#addStockModal').modal('hide');
                } else {
                    console.log('Validation errors:', response.errors);
                    alert('There were errors in your submission.');
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', status, error);
                console.error('Response:', xhr.responseText);
                alert('An error occurred while adding stock: ' + error);
            }
        });
    });
    
    // Update the modal content when it is about to be shown
    $('#addStockModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var itemName = button.attr('data-item-name');
        var itemCategory = button.attr('data-item-category');
        var itemWeight = button.attr('data-item-weight');
        var itemLabel = button.attr('data-item-label');
        var itemOriginstock = button.attr('data-item-origin-stock');
        
        console.log("Grouped - Item Name:", itemName);
        console.log("Grouped - Item Weight:", itemWeight);
        console.log("Grouped - Item Origin Stock:", itemOriginstock);
        
        var modal = $(this);
        modal.find('#modalItemName').text(itemName);
        // Set the hidden input values for form submission:
        modal.find('#groupedModalItemNameHidden').val(itemName);
        modal.find('#groupedModalItemCategory').val(itemCategory);
        modal.find('#groupedModalItemWeight').val(itemWeight);
        modal.find('#groupedModalItemLabel').val(itemLabel);
        modal.find('#groupedModalItemOriginstock').val(itemOriginstock);
    });
});

// Add stock detail
$(document).ready(function() {
    // Handle the form submission using AJAX
    $('#stockdetailForm').on('submit', function(e) {
        console.log("AJAX submit triggered");
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: addStockDetailUrl,
            data: $(this).serialize(),
            success: function(response) {
                if(response.success){
                    alert(response.message);
                    $('#addStockDetailModal').modal('hide');
                } else {
                    console.log('Validation errors:', response.errors);
                    alert('There were errors in your submission.');
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', status, error);
                console.error('Response:', xhr.responseText);
                alert('An error occurred while adding stock: ' + error);
            }
        });
    });
    
    // Update the modal content when it is about to be shown
    $('#addStockDetailModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var itemName = button.attr('data-item-name');
        var itemCategory = button.attr('data-item-category');
        var itemWeight = button.attr('data-item-weight');
        var itemLabel = button.attr('data-item-label');
        var itemOriginstock = button.attr('data-item-origin-stock');
        var itemExpirydate = button.attr('data-item-expiry-date');
        var itemBatch = button.attr('data-item-batch');
        
        console.log("Detail - Item Name:", itemName);
        console.log("Detail - Item Category:", itemCategory);
        console.log("Detail - Item Weight:", itemWeight);
        console.log("Detail - Item Label:", itemLabel);
        console.log("Detail - Item Origin Stock:", itemOriginstock);
        console.log("Detail - Item Expiry Date:", itemExpirydate);
        console.log("Detail - Item Batch:", itemBatch);
        
        var modal = $(this);
        modal.find('#modalItemName').text(itemName);
        // Set the hidden input values for form submission:
        modal.find('#detailModalItemNameHidden').val(itemName);
        modal.find('#detailModalItemCategory').val(itemCategory);
        modal.find('#detailModalItemWeight').val(itemWeight);
        modal.find('#detailModalItemLabel').val(itemLabel);
        modal.find('#detailModalItemOriginstock').val(itemOriginstock);
        modal.find('#detailModalItemExpirydate').val(itemExpirydate);
        modal.find('#detailModalItemBatch').val(itemBatch);
    });
});
