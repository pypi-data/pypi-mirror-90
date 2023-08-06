from localstack.utils.aws import aws_models
Stvyp=super
StvyQ=None
StvyA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Stvyp(LambdaLayer,self).__init__(arn)
  self.cwd=StvyQ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.StvyA.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,StvyA,env=StvyQ):
  Stvyp(RDSDatabase,self).__init__(StvyA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,StvyA,env=StvyQ):
  Stvyp(RDSCluster,self).__init__(StvyA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,StvyA,env=StvyQ):
  Stvyp(AppSyncAPI,self).__init__(StvyA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,StvyA,env=StvyQ):
  Stvyp(AmplifyApp,self).__init__(StvyA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,StvyA,env=StvyQ):
  Stvyp(ElastiCacheCluster,self).__init__(StvyA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,StvyA,env=StvyQ):
  Stvyp(TransferServer,self).__init__(StvyA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,StvyA,env=StvyQ):
  Stvyp(CloudFrontDistribution,self).__init__(StvyA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,StvyA,env=StvyQ):
  Stvyp(CodeCommitRepository,self).__init__(StvyA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
