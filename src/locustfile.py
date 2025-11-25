from locust import HttpUser, task, between

class QuickstartUser(HttpUser):

    @task()
    def add(self):
        for a in range(1,10):
            self.client.get(f"/calc/add?a={a}&b=9", name = "Calc Add Endpoint")
    
    @task()
    def sub(self):
        for a in range(1,10):
            self.client.get(f"/calc/sub?a={a}&b=9", name = "Calc Sub Endpoint")

    @task()
    def mul(self):
        for a in range(1,10):
            self.client.get(f"/calc/mul?a={a}&b=9", name = "Calc Mul Endpoint")

    @task()
    def div(self):
        for a in range(1,10):
            self.client.get(f"/calc/div?a={a}&b=9", name = "Calc Div Endpoint")

    @task()
    def mod(self):
        for a in range(1,10):
            self.client.get(f"/calc/mod?a={a}&b=9", name = "Calc Mod Endpoint")

    @task()
    def random(self):
        for a in range(1,10):
            self.client.get(f"/calc/random?a={a}&b=9", name = "Calc Random Endpoint")

    @task()
    def reduce(self):
        for a in range(1,10):
            self.client.get(f"/calc/reduce?op=add&lst=[{a},9]", name = "Calc Reduce Endpoint")

    @task()
    def lower(self):
        for a in range(1,10):
            self.client.get(f"/str/lower?a=TESTING{a}", name = "String Lower Endpoint")
    @task()
    def upper(self):
        for a in range(1,10):
            self.client.get(f"/str/upper?a=testing{a}", name = "String Upper Endpoint")
    @task()
    def concat(self):
        for a in range(1,10):
            self.client.get(f"/str/concat?a=testing{a}&b=TESTING{a}", name = "String Concat Endpoint")
    
    wait_time = between(1, 2)