vcl 4.0;

backend default {
    .host = "192.168.33.14";
    .port = "9000";
}

sub vcl_recv {
	return (pass);
}

sub vcl_backend_response {
}

sub vcl_deliver {
}
