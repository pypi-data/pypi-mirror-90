class prime_no:
    def is_prime(self,num):
        if num <=1:
            return False
        for x in range(2,num):
            if num%x==0:
                return False
        return True
