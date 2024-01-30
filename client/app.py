import grpc
import users_pb2
import users_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)

        # Create a new user
        new_user = users_pb2.User(id="1", name="omar", email="omar@test.com", password="password")
        create_response = stub.CreateUser(users_pb2.CreateUserRequest(user=new_user))
        print("Created user:", create_response.user)

        # Get all users
        get_users_response = stub.GetUsers(users_pb2.GetUsersRequest())
        print("All users:", get_users_response.users)

        # Get user by ID
        user_id_to_get = "1"
        get_user_by_id_response = stub.GetUserById(users_pb2.GetUserByIdRequest(id=user_id_to_get))
        print(f"User with ID {user_id_to_get}:", get_user_by_id_response.user)

        # Update user
        updated_user = users_pb2.User(id="1", name="Updated Omar", email="omar@example.com", password="new_password")
        update_response = stub.UpdateUser(users_pb2.UpdateUserRequest(user=updated_user))
        print("Updated user:", update_response.user)

        # Delete user
        delete_user_id = "1"
        delete_response = stub.DeleteUser(users_pb2.DeleteUserRequest(id=delete_user_id))
        print("Deleted user:", delete_response.user)

if __name__ == "__main__":
    run()
