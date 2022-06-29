package com.example.remotecontrol;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    Button buttonLeft;
    Button buttonRight;
    Button back;
    Button forward;
    EditText url;
    String urlString;
    public static final String REQUEST_METHOD = "GET";
    public static final int READ_TIMEOUT = 15000;
    public static final int CONNECTION_TIMEOUT = 15000;
    HTTPCall httpCall;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        url = findViewById(R.id.url);
        buttonLeft = findViewById(R.id.button);
        buttonRight = findViewById(R.id.button3);
        back = findViewById(R.id.back);
        forward = findViewById(R.id.frward);

        buttonLeft.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                urlString= url.getText().toString();
                httpCall = new HTTPCall();
                httpCall.stringUrl = "http://"+ urlString+"/L";
                Thread th = new Thread(httpCall);
                th.start();

            }
        });

        buttonRight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                urlString= url.getText().toString();
                httpCall = new HTTPCall();
                httpCall.stringUrl = "http://"+urlString+"/R";
                Thread th = new Thread(httpCall);
                th.start();
            }
        });

        forward.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                urlString= url.getText().toString();
                httpCall = new HTTPCall();
                httpCall.stringUrl = "http://"+urlString+"/F";
                Thread th = new Thread(httpCall);
                th.start();
            }
        });

        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                urlString= url.getText().toString();
                httpCall = new HTTPCall();
                httpCall.stringUrl = "http://"+urlString+"/B";
                Thread th = new Thread(httpCall);
                th.start();
            }
        });
    }

    class HTTPCall implements Runnable
    {
       public String stringUrl;
        @Override
        public void run() {
            try {
                String inputLine;
                //Create a URL object holding our url
                URL myUrl = new URL(stringUrl);
                //Create a connection
                HttpURLConnection connection =(HttpURLConnection)
                        myUrl.openConnection();
                //Set methods and timeouts
                connection.setRequestMethod(REQUEST_METHOD);
                connection.setReadTimeout(READ_TIMEOUT);
                connection.setConnectTimeout(CONNECTION_TIMEOUT);

                //Connect to our url
                connection.connect();
                //Create a new InputStreamReader
                InputStreamReader streamReader = new
                        InputStreamReader(connection.getInputStream());
                //Create a new buffered reader and String Builder
                BufferedReader reader = new BufferedReader(streamReader);
                StringBuilder stringBuilder = new StringBuilder();
                //Check if the line we are reading is not null
                while((inputLine = reader.readLine()) != null){
                    stringBuilder.append(inputLine);
                }
                //Close our InputStream and Buffered reader
                reader.close();
                streamReader.close();
                //Set our result equal to our stringBuilder
                String result = stringBuilder.toString();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}