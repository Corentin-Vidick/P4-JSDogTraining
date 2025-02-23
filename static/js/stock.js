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
        
        console.log("Item Name:", itemName);
        console.log("Item Weight:", itemWeight);
        console.log("Item Origin Stock:", itemOriginstock);
        
        var modal = $(this);
        modal.find('#modalItemName').text(itemName);
        // Set the hidden input values for form submission:
        modal.find('#modalItemNameHidden').val(itemName);
        modal.find('#modalItemCategory').val(itemCategory);
        modal.find('#modalItemWeight').val(itemWeight);
        modal.find('#modalItemLabel').val(itemLabel);
        modal.find('#modalItemOriginstock').val(itemOriginstock);
    });
});
