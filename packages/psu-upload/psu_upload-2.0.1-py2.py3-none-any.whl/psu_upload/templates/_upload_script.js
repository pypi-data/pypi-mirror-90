
function dndHoverStyles(){
    $('.dnd-input').on('dragenter', function(){
        $(this).addClass('dnd-input-hover');
    });
    $('input[type=file]').on('dragleave', function(){
        $(this).removeClass('dnd-input-hover');
    });
}


/** handle_file_selection()
 *  Resize and upload all selected files from one input
 *********************************************************/
function handle_file_selection(input, upload_url){

    // Get the file input name
    let input_name = input.attr('name');
    let id = input.attr('id');

    // Get all files from the input (if multiple="true")
    let files = input.prop('files');

    //Prepare file list display elements
    let files_container = $('#' + input_name + '_files_container');
    if(files_container.length == 0){
        input.after(`
            <div id="${input_name}_files_container" class="dnd-status-container hidden">
                <b>Uploaded Files</b>:
                <ol class="dnd-file-list"></ol>
            </div>
        `);
        files_container = $('#' + input_name + '_files_container');
    }
    let file_list = files_container.find('ol');
    if(file_list.length == 0){
        files_container.append(`<ol class="dnd-file-list"></ol>`);
        file_list = files_container.find('ol');
    }

    //Resize each image and upload (individually)
    ([...files]).forEach(function(file_instance) {
        // Get the actual file name of the uploaded file to display on the browser
        let file_name = file_instance.name;

        //Add file to file list
        files_container.removeClass('hidden');
        let file_seq = file_list.find('li').length + 1;
        let li = `<li id="li-fs-${file_seq}"><span class="file_name">${file_name}</span><span class="file_status"></span></li>`;
        file_list.append(li);

        //Get status container
        let status_container = file_list.find(`#li-fs-${file_seq}`).find('.file_status');

        //Status indicators
        let upload_ind = '<span class="upload_ind text-info"><i class="fa fa-spinner fa-pulse fa-1x fa-fw" ></i> Uploading...</span>';
        let success_ind = '<span class="upload_ind text-success"><i class="fa fa-check fa-1x fa-fw" ></i></span>';
        let error_ind = '<span class="upload_ind text-danger"><i class="fa fa-exclamation-triangle fa-1x fa-fw" ></i></span>';

        //Resize image (if applicable), then...
        resizeImage(input, file_instance, 1000, 50, status_container).then((resized_image)=>{

            // Create a new FormData object
            let formData = new FormData();

            // Add CSRF token (required for all POST requests)
            formData.append('csrfmiddlewaretoken', '{{csrf_token}}');

            //Add the input name
            formData.append('input_name', input_name);

            // Add resized file to the FormData
            formData.append(input_name, resized_image);

            $.ajax({
                type:   "POST",
                url:    upload_url,
                data:   formData,
                processData: false,
                contentType: false,
                beforeSend:function(){
                    status_container.html(upload_ind);
                },
                success:function(data){
                    status_container.html(success_ind);
                },
                error:function(data){
                    status_container.html(error_ind);
                },
                complete:function(){}
            });
        });
    });
    input.val('');
}

/** resizeImage()
 *  Resizes a single file
 *      - maxDeviation is the difference that is allowed default: 50kb
 *        Example: targetFileSizeKb = 500 then result will be between 450kb
 *        and 500kb increase the deviation to reduce the amount of iterations.
 ********************************************************************/
async function resizeImage(input, dataUrl, targetFileSizeKb, maxDeviation, status_container){
    let originalFile = dataUrl;

    //Only resize image files greater than specified size
    let imageTypes = ['image/jpeg', 'image/gif', 'image/png'];
    if((!imageTypes.includes(dataUrl.type))||(originalFile.size / 1000 < targetFileSizeKb)){
        return dataUrl;
    }

    // Add resizing indicator when the image is being resized
    let resize_ind = '<span class="upload_ind text-info"><i class="fa fa-spinner fa-pulse fa-1x fa-fw" ></i> Resizing...</span>';
    if(typeof status_container === 'undefined'){
        input.after(resize_ind);
    }
    else{
        status_container.html(resize_ind);
    }

    let low = 0.0;
    let middle = 0.5;
    let high = 1.0;
    let result = dataUrl;
    let file = originalFile;

    // Image will be resize multiple times to get to the target file size
    while(Math.abs(file.size / 1000 - targetFileSizeKb) > maxDeviation){
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        const img = document.createElement('img');
        const promise = new Promise((resolve, reject) => {
            img.onload = () => resolve();
            img.onerror = reject;
        });

        async function readFileAsDataURL(file) {
            let result_base64 = await new Promise((resolve) => {
                let fileReader = new FileReader();
                fileReader.onload = (e) => resolve(fileReader.result);
                fileReader.readAsDataURL(file);
            });

            return result_base64;
        }

        // read file to Data URL using base-64
        let dataURL = await readFileAsDataURL(dataUrl);
        img.src=dataURL;
        await promise;
        canvas.width = Math.round(img.width * middle);
        canvas.height = Math.round(img.height * middle);
        context.scale(canvas.width / img.width, canvas.height / img.height);
        context.drawImage(img, 0, 0);
        file = await urlToFile(canvas.toDataURL(),'test.png','image/png');
        if(file.size/1000 < (targetFileSizeKb - maxDeviation)){
            low = middle;
        }
        else if(file.size/1000 > targetFileSizeKb){
            high = middle;
        }
        middle = (low+high)/2;
        result = canvas.toDataURL();
    }
    // convert URL to a file
    res= await urlToFile(result,'result.png','image/png');

    // Remove the resizing indicator
    if(typeof status_container === 'undefined'){
        input.parent().find('.upload_ind').remove();
    }
    else{
        status_container.html('');
    }
    return res;
}

// Used by resizeImage()
function urlToFile(url, filename, mimeType){
    return (fetch(url)
        .then(function(res){return res.arrayBuffer();})
        .then(function(buf){return new File([buf], filename,{type:mimeType});})
    );
}


$(document).ready(function(){
    dndHoverStyles();
});