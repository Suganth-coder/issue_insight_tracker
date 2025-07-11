class ErrorHandling:
    def GeneralErrorHandler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                print(f"An error occurred: {e}")
                
        return wrapper