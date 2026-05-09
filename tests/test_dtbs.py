from mauri.models.dtbs import conn_dtbs

def test_conn_dtbs():
    conn = conn_dtbs()
    assert conn is not None
    conn.close()