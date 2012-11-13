
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
	    name:album.fields.name
	}
        var template = _.template( $("#album").html(), variables);
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
	"page/:number/show/:count": "process",
    },
    process:function(number, count){
	console.log("page-"+number + " show-"+count);
	var data = {page: number, show: count};
	var totalRows = parseInt(count/3, 10);
	if (count/3>totalRows){
	    totalRows = totalRows + 1;
	}
	console.log(totalRows);
	create_album_row(totalRows);
	App.get_raw_data("/album/objects", data, function(data){
	    for (i in data){
		create_album_cover(data[i], parseInt(i/3, 10));
	    }
	}, "album-loader");
	
	
    }
});
function create_album_row(totalRows){
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

var album_router = new AlbumRouter;
Backbone.history.start();
