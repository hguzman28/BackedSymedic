pipeline {
   agent any
   tools {
         jdk 'java8.1'
         gradle 'GradelApp'
         nodejs 'Nodejsapp'
      }
   

   
   stages {
            
      
      stage('NPM Setup') {
      steps {
         sh 'ionic npm install -g @ionic/cli && npm i -g cordova'
     

         
      }
   }
      
      stage('Insntall npm i angular-code-input'){
         
         steps{
            
            sh 'npm i angular-code-input'
         
         }
      
      
      }
      
  
    
      
     
   stage('Android Build') {
   steps {
      sh 'ionic cordova build android --release'
   
   }
  }

   stage('APK Sign') {
   steps {
      sh 'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -storepass "j@mar2021" -keystore ./jamar.keystore platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk jamar'
   }
   }
      
      stage('Test QA - Disenable'){
         
         parallel {
            
            stage('Code Analysis '){
               steps {   
                  echo 'Code Analysis '
                  }   
               }
            
             stage('JUnit Test'){
               steps {   
                  echo 'JUnit Test'
                  }   
               }
            
             stage('Performance'){
               steps {   
                  echo 'Performance'
                  }   
               }
         
         
         
         }
         
      
      }  

  
   stage('Deploy APK Main') {
      
     when {
        branch 'main'
     }
      
     steps {
       
       sh '$ANDROID_HOME/build-tools/28.0.3/zipalign -v 4 platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk ./appVenta_${BRANCH_NAME}_${BUILD_NUMBER}.apk'

        // Send notifications Teams
        office365ConnectorSend webhookUrl: 'https://organizacionjamar.webhook.office.com/webhookb2/2f1970e2-7e84-4055-94bd-00391026fdc7@25ec7cf2-a9a8-4e2c-a7b4-ac2de2935167/JenkinsCI/b2f27ca03f28468cb9fe2186fc592c42/72d4ed85-9c48-4db3-b606-9989895547e3',
           message: 'Application has been Success ${ env.BRANCH_NAME }',
            status: 'Success'      
      }
     }
      
      
    stage('Deploy APK Dev') {
       
     when {
        branch 'dev'
     }  
            
     steps {
       
        
       sh '$ANDROID_HOME/build-tools/28.0.3/zipalign -v 4 platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk ./appVenta_${BRANCH_NAME}_${BUILD_NUMBER}.apk'

        // Send notifications Teams
        office365ConnectorSend webhookUrl: 'https://organizacionjamar.webhook.office.com/webhookb2/2f1970e2-7e84-4055-94bd-00391026fdc7@25ec7cf2-a9a8-4e2c-a7b4-ac2de2935167/JenkinsCI/42769e9d7a0d4ff38678d1c5ca675d4f/72d4ed85-9c48-4db3-b606-9989895547e3',
           message: 'Application has been Success ${env.GIT_COMMIT}',
            status: 'Success'      
      }
     }
      
    stage('Deploy APK QAS') {
       
     when {
        branch 'qa'
     }  
     steps {
        
       sh '$ANDROID_HOME/build-tools/28.0.3/zipalign -v 4 platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk ./appVenta_${BRANCH_NAME}_${BUILD_NUMBER}.apk'

        // Send notifications Teams
        office365ConnectorSend webhookUrl: 'https://organizacionjamar.webhook.office.com/webhookb2/2f1970e2-7e84-4055-94bd-00391026fdc7@25ec7cf2-a9a8-4e2c-a7b4-ac2de2935167/JenkinsCI/48290fede8694af5990153df8d44ce41/72d4ed85-9c48-4db3-b606-9989895547e3',
           message: 'Application has been Success',
            status: 'Success'      
      }
     }
      
      stage ('Deploy Piloto'){
         
         when {
            
            branch 'backup-dev-25Abril23'
         
         }
         
         steps {
            sh '$ANDROID_HOME/build-tools/28.0.3/zipalign -v 4 platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk ./appVenta.apk'

            sh 'ruby upload_apk.rb'
         
         }
      
      
      }  
      
      
  
      

     

 }
   
    post{
       
       always{
          
          archiveArtifacts artifacts: "appVenta_${env.BRANCH_NAME}_${env.BUILD_NUMBER}.apk" 
         
       
       }
       
       failure{
          
         // some instructions here #
         office365ConnectorSend webhookUrl: 'https://organizacionjamar.webhook.office.com/webhookb2/2f1970e2-7e84-4055-94bd-00391026fdc7@25ec7cf2-a9a8-4e2c-a7b4-ac2de2935167/JenkinsCI/b2f27ca03f28468cb9fe2186fc592c42/72d4ed85-9c48-4db3-b606-9989895547e3',
         message: 'Application has been Failure',
         status: 'Failure'   
       
       
       }

    }
   

}
