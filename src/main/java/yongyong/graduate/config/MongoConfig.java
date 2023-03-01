package yongyong.graduate.config;

import com.mongodb.client.MongoClient;
import org.springframework.boot.autoconfigure.mongo.MongoProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.data.mongodb.MongoDatabaseFactory;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.SimpleMongoClientDatabaseFactory;
import org.springframework.data.mongodb.core.SimpleMongoClientDbFactory;

@Configuration
public class MongoConfig {
    @Primary
    @Bean(name = "db1Properties")
    @ConfigurationProperties(prefix = "spring.data.mongodb.db1")
    public MongoProperties getDb1Props() throws Exception {
        return new MongoProperties();
    }

    @Bean(name = "db2Properties")
    @ConfigurationProperties(prefix = "spring.data.mongodb.db2")
    public MongoProperties getDb2Props() throws Exception {
        return new MongoProperties();
    }

    @Primary
    @Bean(name = "db1MongoTemplate")
    public MongoTemplate db1MongoTemplate() throws Exception {
        return new MongoTemplate(db1MongoDatabaseFactory(getDb1Props()));
    }

    @Primary
    @Bean
    public MongoDatabaseFactory db1MongoDatabaseFactory(MongoProperties mongo) throws Exception {
        System.out.println(mongo.getUri());
        return new SimpleMongoClientDatabaseFactory(
                mongo.getUri()
        );
    }

    @Bean(name = "db2MongoTemplate")
    public MongoTemplate db2MongoTemplate() throws Exception {
        return new MongoTemplate(db2MongoDatabaseFactory(getDb2Props()));
    }

    @Bean
    public MongoDatabaseFactory db2MongoDatabaseFactory(MongoProperties mongo) throws Exception {
        System.out.println(mongo.getUri());
        return new SimpleMongoClientDatabaseFactory(
                mongo.getUri()
        );
    }
}