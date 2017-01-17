class Ghost3Dblock:
    def  __init__(self):
        self.id = -1
        self.proc_id= -1
        self.neighbors = []
        self.data = 0
        self.wait_off = 0
        self.wait_on = 1
        self.loaded = 0
        self.processed = 0
        self.receiving = 0
        self.sending = 0
        self.dirty = -1
        self.faces = []
        self.queued = False
        self.dependencies = 0


