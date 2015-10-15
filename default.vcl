backend default {
    .host = "i192.168.33.14";
    .port = "9000";
}

sub vcl_recv {
	return (pass);
}

sub vcl_backend_response {
}

sub vcl_deliver {
}
