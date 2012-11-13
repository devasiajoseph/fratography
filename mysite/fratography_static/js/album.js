
var AlbumCover = Backbone.View.extend({
    initialize:function(attrs){
	this.options = attrs;
	this.render();
	
    },
    render:function(){
	
	// Compile the template using underscore
	var album = this.options.album;
	var variables = {
	    cover_photo:album.fields.cover_photo,
	    name:album.fields.name,
	    album_id:album.pk
	}
        var template = _.template( $("#album").html(), variables);
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
    }
    
});
var AlbumPhoto = Backbone.View.extend({
    initialize:function(attrs){
	this.options = attrs;
	this.render();
	
    },
    render:function(){
	
	// Compile the template using underscore
	var photo = this.options.photo;
	var variables = {
	    thumbnail:photo.fields.thumbnail,
	}
        var template = _.template( $("#album-photo").html(), variables);
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
    }
    
});

var AlbumsRow = Backbone.View.extend({
    el:$('#albums-container'),
    initialize:function(attrs){
	this.options = attrs;
	this.render();
    },
    render:function(){
	// Compile the template using underscore
	var variables = {id:this.options.id}
        var template = _.template( $("#albums-row").html(), variables);
        // Load the compiled HTML into the Backbone "el"
        this.$el.append( template );
    }
});

var AlbumRouter = Backbone.Router.extend({
    routes: {
	"page/:number/show/:count": "processAlbums",
	"album/:album_id/page/:number/show/:count": "processPhotos"
    },
    processAlbums:function(number, count){
	console.log("page-"+number + " show-"+count);
	$("#albums-container").html("");
	var data = {page: number, show: count};
	
	create_album_row(count);
	App.get_raw_data("/album/objects", data, function(data){
	    for (i in data){
		create_album_cover(data[i], parseInt(i/3, 10));
	    }
	}, "album-loader");
	
	
    },
    processPhotos:function(album_id, number, count){
	console.log("page-"+number + " show-"+count);
	$("#albums-container").html("");
	var data = {page: number, show: count, album_id:album_id};
	
	create_album_row(count);
	App.get_raw_data("/album/photos", data, function(data){
	    for (i in data){
		create_album_photo(data[i], parseInt(i/4, 10));
	    }
	}, "album-loader");
	
    }
});
function create_album_row(count){
    
    var totalRows = parseInt(count/3, 10);
    if (count/3>totalRows){
	totalRows = totalRows + 1;
    }
    console.log(totalRows);
    for(i=0;i<totalRows;i++){
	var album_row = new AlbumsRow({"id":i});
    }
}

function create_album_cover(album, row_id){
    console.log(album.fields.cover_photo);
    var album_cover = new AlbumCover({
	el: $("#albums-row-"+row_id),
	"album":album});
}
function create_album_photo(photo, row_id){
    var album_photo = new AlbumPhoto({
	el: $("#albums-row-"+row_id),
	"photo":photo});
}

var album_router = new AlbumRouter;
Backbone.history.start();
