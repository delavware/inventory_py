class UserModel:
    def __init__(self):
        # Simulación de un usuario y contraseña
        # En una aplicación real, las contraseñas deberían estar hasheadas
        self.valid_username = "admin"
        self.valid_password = "1234"

    def authenticate_user(self, username, password):
        """
        Simula la autenticación de un usuario verificando las credenciales.
        
        Args:
            username (str): El nombre de usuario proporcionado.
            password (str): La contraseña proporcionada.
            
        Returns:
            bool: True si las credenciales son válidas, False en caso contrario.
        """
        return username == self.valid_username and password == self.valid_password

