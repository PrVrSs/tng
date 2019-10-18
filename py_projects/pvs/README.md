# pvs - python video server

**Now it's: Python HLS/DASH adaptive streaming server**


### Requirements
* latest version of python(python 3.7)


### Quickstart
```text
TODO
```

### Tools

* [HLS/DASH cutter](pvs/tools/cutter)

### Roadmap

- [ ] Live Streaming
- [ ] EPG
- [ ] Session and registration 
- [ ] Docker
- [ ] ReStreaming from another resources/services
- [ ] Improve Converter
- [ ] support PostgreSQL
- [ ] Expand type support 
   - [ ] HTTP-FLV
   - [ ] RTMP
   - [ ] WS-FLV
- [ ] CI(travis)
- [ ] webrtc
- [ ] quickstart
- [ ] ML
- [ ] no server side
   - [ ] Frontend (React)
   - [ ] GUI (PyQt5 or kivy

```
gunicorn 'pvs.__main__:init_app("pvs/config.ini")' -c pvs/gunicorn.conf.py
```