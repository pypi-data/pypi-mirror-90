========
Examples
========

To use PyOpenVidu in a project, first import it::

    from pyopenvidu import OpenVidu

Create a session::

    openvidu = OpenVidu(OPENVIDU_URL, OPENVIDU_SECRET)
    session = openvidu.create_session()

Generate a token a session::

    token = session.create_webrtc_connection().token

Fetch information::

    # Fetch all session info from OpenVidu Server
    openvidu.fetch()
    sessions = openvidu.sessions  # sessions returns a list of OpenViduSession objects

    # Fetch a specific session info from the server
    session.fetch()
    connections = session.connections

    # Fetch a specific connection info from the server
    connection.fetch()
    subs = connection.subscribers


Send signals::

    # Broadcast signal to session
    session.signal("MY_TYPE", "Hello world!")

    # Send to a specific connection
    session.get_connection("vhdxz7abbfirh2lh").signal("MY_TYPE", "Hello other world!")


    # Send to every other connection
    # Note: This does not make any subsequent API calls, as the connections information is already stored in memory
    session.signal("MY_TYPE", "Yolo world!", [conn for i, conn in enumerate(session.connections) if i % 2 == 0])

Connect to IP camera::

    session.create_ipcam_connection("rtsp://mydomain.net:1935/live/stream")

Close a session::

    session.close()

Force disconnect users::

    # Disconnect a specific user
    # None: Don't forget to call session.fetch() to work with the updated list of clients
    session.get_connection("vhdxz7abbfirh2lh").force_disconnect()

    # Disconnect every other user
    # Note: This does not make any subsequent API calls, as the connections information is already stored in memory
    for i, conn in enumerate(session.connections):
        if i % 2 == 0:
            conn.force_disconnect()

    # session.fetch() Should be called about here.

Force unpublish an user's streams::

    # Unpublish a single stream (most of the time there is only one, except when sharing screen):
    session.get_connection("vhdxz7abbfirh2lh").publishers[0].force_unpublish()

    # Unpublish all streams of an user:
    session.get_connection("vhdxz7abbfirh2lh").force_unpublish_all_streams()

