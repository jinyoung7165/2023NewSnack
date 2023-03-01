package yongyong.graduate.config;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@Configuration
@EnableMongoRepositories(basePackages = {"yongyong.graduate.hotDomain"},
mongoTemplateRef = Db1Config.MONGO_TEMPLATE)
@EnableConfigurationProperties
public class Db1Config {
    protected static final String MONGO_TEMPLATE = "db1MongoTemplate";
}