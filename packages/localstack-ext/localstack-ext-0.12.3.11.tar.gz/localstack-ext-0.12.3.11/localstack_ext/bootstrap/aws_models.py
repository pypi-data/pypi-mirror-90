from localstack.utils.aws import aws_models
iRbrT=super
iRbrv=None
iRbrl=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  iRbrT(LambdaLayer,self).__init__(arn)
  self.cwd=iRbrv
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.iRbrl.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,iRbrl,env=iRbrv):
  iRbrT(RDSDatabase,self).__init__(iRbrl,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,iRbrl,env=iRbrv):
  iRbrT(RDSCluster,self).__init__(iRbrl,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,iRbrl,env=iRbrv):
  iRbrT(AppSyncAPI,self).__init__(iRbrl,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,iRbrl,env=iRbrv):
  iRbrT(AmplifyApp,self).__init__(iRbrl,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,iRbrl,env=iRbrv):
  iRbrT(ElastiCacheCluster,self).__init__(iRbrl,env=env)
class TransferServer(BaseComponent):
 def __init__(self,iRbrl,env=iRbrv):
  iRbrT(TransferServer,self).__init__(iRbrl,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,iRbrl,env=iRbrv):
  iRbrT(CloudFrontDistribution,self).__init__(iRbrl,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,iRbrl,env=iRbrv):
  iRbrT(CodeCommitRepository,self).__init__(iRbrl,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
