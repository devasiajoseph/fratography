function displayImage(image, id){
    $("#lightbox-test").trigger('close');
    $("#image-display-container").html('<img src="'+image+'" id="display-image"  style="width:100%">');
    $("#lightbox-test").lightbox_me();
    $("#id_selected_image").val(id);
}
