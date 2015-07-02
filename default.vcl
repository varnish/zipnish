backend default {
    .host = "127.0.0.1";
    .port = "9000";
}

sub vcl_recv {
	return (pass);
}

sub vcl_backend_response {
}

sub vcl_deliver {
}
