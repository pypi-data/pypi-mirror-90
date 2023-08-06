from localstack.utils.aws import aws_models
LSkmD=super
LSkmj=None
LSkmC=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  LSkmD(LambdaLayer,self).__init__(arn)
  self.cwd=LSkmj
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.LSkmC.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,LSkmC,env=LSkmj):
  LSkmD(RDSDatabase,self).__init__(LSkmC,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,LSkmC,env=LSkmj):
  LSkmD(RDSCluster,self).__init__(LSkmC,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,LSkmC,env=LSkmj):
  LSkmD(AppSyncAPI,self).__init__(LSkmC,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,LSkmC,env=LSkmj):
  LSkmD(AmplifyApp,self).__init__(LSkmC,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,LSkmC,env=LSkmj):
  LSkmD(ElastiCacheCluster,self).__init__(LSkmC,env=env)
class TransferServer(BaseComponent):
 def __init__(self,LSkmC,env=LSkmj):
  LSkmD(TransferServer,self).__init__(LSkmC,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,LSkmC,env=LSkmj):
  LSkmD(CloudFrontDistribution,self).__init__(LSkmC,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,LSkmC,env=LSkmj):
  LSkmD(CodeCommitRepository,self).__init__(LSkmC,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
