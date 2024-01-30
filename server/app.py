from concurrent import futures
import grpc
import users_pb2
import users_pb2_grpc

class Users(users_pb2_grpc.UserService):
    def __init__(self):
        self.user_database = []

    def GetUsers(self, request, context):
        return users_pb2.GetUsersResponse(users=self.user_database)

    def GetUserById(self, request, context):
        user_id = request.id
        for user in self.user_database:
            if user.id == user_id:
                return users_pb2.GetUserByIdResponse(user=user)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("User not found")
        return users_pb2.GetUserByIdResponse()

    def CreateUser(self, request, context):
        new_user = request.user
        self.user_database.append(new_user)
        return users_pb2.CreateUserResponse(user=new_user)

    def UpdateUser(self, request, context):
        updated_user = request.user
        for i, user in enumerate(self.user_database):
            if user.id == updated_user.id:
                self.user_database[i] = updated_user
                return users_pb2.UpdateUserResponse(user=updated_user)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("User not found")
        return users_pb2.UpdateUserResponse()

    def DeleteUser(self, request, context):
        user_id = request.id
        for i, user in enumerate(self.user_database):
            if user.id == user_id:
                deleted_user = self.user_database.pop(i)
                return users_pb2.DeleteUserResponse(user=deleted_user)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("User not found")
        return users_pb2.DeleteUserResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserServiceServicer_to_server(Users(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
